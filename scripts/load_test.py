"""
T07GPTcodeDetect - Load Test Script
====================================
Test khả năng chịu tải của hệ thống với nhiều concurrent users.

Cách chạy:
    python scripts/load_test.py
    python scripts/load_test.py --url http://localhost:8000
    python scripts/load_test.py --url http://localhost:8000 --max-users 50
"""

import asyncio
import aiohttp
import time
import argparse
import statistics
import sys
import io
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
BASE_URL = "http://localhost:8000"
TIMEOUT_SEC = 30          # Timeout mỗi request
REQUESTS_PER_LEVEL = 20   # Số requests gửi ở mỗi mức concurrency

CONCURRENCY_LEVELS = [1, 2, 5, 10, 20, 30, 50]  # Số concurrent users

# Code Python ngắn để test ML inference (consistent)
TEST_CODE_PYTHON = """\
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

result = bubble_sort([64, 34, 25, 12, 22, 11, 90])
print(result)
"""

TEST_CODE_JAVA = """\
public class BubbleSort {
    public static int[] sort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
        return arr;
    }
}
"""


# ─────────────────────────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────────────────────────
@dataclass
class RequestResult:
    success: bool
    status_code: int
    response_time_ms: float
    error: Optional[str] = None


@dataclass
class LevelResult:
    concurrency: int
    results: List[RequestResult] = field(default_factory=list)

    @property
    def total(self): return len(self.results)

    @property
    def success_count(self): return sum(1 for r in self.results if r.success)

    @property
    def error_count(self): return self.total - self.success_count

    @property
    def success_rate(self):
        return (self.success_count / self.total * 100) if self.total else 0

    @property
    def times(self):
        return [r.response_time_ms for r in self.results if r.success]

    @property
    def avg_ms(self): return statistics.mean(self.times) if self.times else 0

    @property
    def min_ms(self): return min(self.times) if self.times else 0

    @property
    def max_ms(self): return max(self.times) if self.times else 0

    @property
    def p95_ms(self):
        if not self.times: return 0
        s = sorted(self.times)
        idx = int(len(s) * 0.95)
        return s[min(idx, len(s) - 1)]

    @property
    def p99_ms(self):
        if not self.times: return 0
        s = sorted(self.times)
        idx = int(len(s) * 0.99)
        return s[min(idx, len(s) - 1)]

    @property
    def throughput_rps(self):
        if not self.times: return 0
        total_time_sec = sum(self.times) / 1000
        return self.success_count / total_time_sec if total_time_sec > 0 else 0


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def color(text, code): return f"\033[{code}m{text}\033[0m"
def green(t): return color(t, "92")
def red(t): return color(t, "91")
def yellow(t): return color(t, "93")
def cyan(t): return color(t, "96")
def bold(t): return color(t, "1")
def dim(t): return color(t, "2")

def bar(value, max_val, width=20, fill="█"):
    if max_val == 0: return " " * width
    filled = int(value / max_val * width)
    return fill * filled + "░" * (width - filled)

def ms_color(ms):
    if ms < 500:   return green(f"{ms:7.0f}ms")
    if ms < 2000:  return yellow(f"{ms:7.0f}ms")
    return red(f"{ms:7.0f}ms")

def rate_color(rate):
    if rate >= 99: return green(f"{rate:.1f}%")
    if rate >= 90: return yellow(f"{rate:.1f}%")
    return red(f"{rate:.1f}%")

def print_header(title):
    print()
    print(bold(cyan("═" * 68)))
    print(bold(cyan(f"  {title}")))
    print(bold(cyan("═" * 68)))

def print_section(title):
    print()
    print(bold(f"  ┌─ {title}"))


# ─────────────────────────────────────────────────────────────
# REQUEST FUNCTIONS
# ─────────────────────────────────────────────────────────────
async def request_health(session: aiohttp.ClientSession, base_url: str) -> RequestResult:
    start = time.perf_counter()
    try:
        async with session.get(f"{base_url}/health") as resp:
            elapsed = (time.perf_counter() - start) * 1000
            return RequestResult(
                success=resp.status == 200,
                status_code=resp.status,
                response_time_ms=elapsed
            )
    except asyncio.TimeoutError:
        elapsed = (time.perf_counter() - start) * 1000
        return RequestResult(success=False, status_code=0, response_time_ms=elapsed, error="Timeout")
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        return RequestResult(success=False, status_code=0, response_time_ms=elapsed, error=str(e)[:60])


async def request_analysis(session: aiohttp.ClientSession, base_url: str, lang: str = "python") -> RequestResult:
    code = TEST_CODE_PYTHON if lang == "python" else TEST_CODE_JAVA
    payload = {
        "code": code,
        "language": lang,
        "model": "auto",
        "save_to_history": False
    }
    start = time.perf_counter()
    try:
        async with session.post(
            f"{base_url}/api/analysis",
            json=payload
        ) as resp:
            elapsed = (time.perf_counter() - start) * 1000
            await resp.json()  # consume body
            return RequestResult(
                success=resp.status == 200,
                status_code=resp.status,
                response_time_ms=elapsed
            )
    except asyncio.TimeoutError:
        elapsed = (time.perf_counter() - start) * 1000
        return RequestResult(success=False, status_code=0, response_time_ms=elapsed, error="Timeout")
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        return RequestResult(success=False, status_code=0, response_time_ms=elapsed, error=str(e)[:60])


# ─────────────────────────────────────────────────────────────
# LOAD LEVEL RUNNER
# ─────────────────────────────────────────────────────────────
async def run_level(
    base_url: str,
    concurrency: int,
    n_requests: int,
    endpoint: str,
    semaphore: asyncio.Semaphore
) -> LevelResult:
    level = LevelResult(concurrency=concurrency)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SEC)

    async def do_request(session):
        async with semaphore:
            if endpoint == "health":
                result = await request_health(session, base_url)
            else:
                result = await request_analysis(session, base_url)
            level.results.append(result)
            # Live progress
            sym = green("✓") if result.success else red("✗")
            print(f"    {sym}", end="", flush=True)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [do_request(session) for _ in range(n_requests)]
        await asyncio.gather(*tasks)

    print()  # newline after progress dots
    return level


# ─────────────────────────────────────────────────────────────
# WARM-UP
# ─────────────────────────────────────────────────────────────
async def warmup(base_url: str) -> bool:
    print_section("Warm-up: kiểm tra server đang chạy...")
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{base_url}/health") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"  │  {green('✓')} Server OK — {data.get('app', '?')} v{data.get('version', '?')}")
                    return True
                else:
                    print(f"  │  {red('✗')} Server trả về HTTP {resp.status}")
                    return False
    except Exception as e:
        print(f"  │  {red('✗')} Không kết nối được: {e}")
        print(f"  │  Hãy đảm bảo server đang chạy tại {base_url}")
        return False


async def measure_baseline(base_url: str) -> tuple:
    """Đo latency baseline với 1 request đơn lẻ"""
    print_section("Đo baseline latency (1 request)...")
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SEC)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Health
        h = await request_health(session, base_url)
        # ML Analysis x3 lấy trung bình (vì lần đầu có thể load model)
        times = []
        for _ in range(3):
            r = await request_analysis(session, base_url)
            if r.success:
                times.append(r.response_time_ms)

        avg_ml = statistics.mean(times) if times else 0
        print(f"  │  Health check:   {ms_color(h.response_time_ms)}")
        print(f"  │  ML Analysis:    {ms_color(avg_ml)}  (avg of {len(times)} requests)")
        return h.response_time_ms, avg_ml


# ─────────────────────────────────────────────────────────────
# MAIN TESTS
# ─────────────────────────────────────────────────────────────
async def run_health_test(base_url: str, levels: List[int]) -> List[LevelResult]:
    """Test /health endpoint — đo overhead server thuần túy"""
    print_section("Test 1 — /health endpoint (không có ML)")
    print(f"  │  {dim('Đo overhead server, database, network thuần túy')}")
    results = []
    for c in levels[:5]:  # Health endpoint test chỉ cần 5 levels
        n = REQUESTS_PER_LEVEL * 2  # nhiều hơn vì fast endpoint
        sem = asyncio.Semaphore(c)
        print(f"  │  {cyan(f'[{c:3d} users]')} gửi {n} requests... ", end="", flush=True)
        lvl = await run_level(base_url, c, n, "health", sem)
        results.append(lvl)
    return results


async def run_analysis_test(base_url: str, levels: List[int]) -> List[LevelResult]:
    """Test /api/analysis endpoint — ML inference load"""
    print_section("Test 2 — /api/analysis endpoint (ML Inference)")
    print(f"  │  {dim('Đo khả năng chịu tải của ML model inference')}")
    results = []
    for c in levels:
        n = REQUESTS_PER_LEVEL
        sem = asyncio.Semaphore(c)
        print(f"  │  {cyan(f'[{c:3d} users]')} gửi {n} requests... ", end="", flush=True)
        lvl = await run_level(base_url, c, n, "analysis", sem)
        results.append(lvl)
        # Dừng sớm nếu success rate < 50%
        if lvl.success_rate < 50 and c > 1:
            print(f"  │  {yellow('⚠ Success rate < 50%, dừng ramp-up sớm')}")
            break
    return results


# ─────────────────────────────────────────────────────────────
# REPORT
# ─────────────────────────────────────────────────────────────
def print_results_table(results: List[LevelResult], title: str):
    print_header(f"KẾT QUẢ: {title}")

    # Table header
    print(f"\n  {'Users':>6}  {'Success':>8}  {'Avg':>9}  {'Min':>9}  {'P95':>9}  {'Max':>9}  {'RPS':>6}  Bar (Avg latency)")
    print(f"  {'─'*6}  {'─'*8}  {'─'*9}  {'─'*9}  {'─'*9}  {'─'*9}  {'─'*6}  {'─'*22}")

    max_avg = max((r.avg_ms for r in results if r.times), default=1)

    for r in results:
        if not r.times:
            print(f"  {r.concurrency:>6}  {rate_color(0):>8}  {'N/A':>9}  {'N/A':>9}  {'N/A':>9}  {'N/A':>9}  {'0.0':>6}  {red('ALL FAILED')}")
            continue

        users_str = f"{r.concurrency:>6}"
        succ_str = rate_color(r.success_rate)
        avg_str = ms_color(r.avg_ms)
        min_str = dim(f"{r.min_ms:7.0f}ms")
        p95_str = ms_color(r.p95_ms)
        max_str = ms_color(r.max_ms)
        rps_str = f"{r.throughput_rps:>6.1f}"
        b = bar(r.avg_ms, max_avg)

        print(f"  {users_str}  {succ_str:>8}  {avg_str}  {min_str}  {p95_str}  {max_str}  {rps_str}  {b}")


def print_summary(health_results: List[LevelResult], ml_results: List[LevelResult]):
    print_header("TỔNG KẾT & ĐÁNH GIÁ")

    # Find breaking points
    ml_ok = [r for r in ml_results if r.success_rate >= 99]
    ml_degraded = [r for r in ml_results if 80 <= r.success_rate < 99]
    ml_broken = [r for r in ml_results if r.success_rate < 80]

    max_stable = ml_ok[-1].concurrency if ml_ok else 0
    max_degraded = ml_degraded[-1].concurrency if ml_degraded else 0

    print(f"\n  {bold('PHÂN TÍCH KIẾN TRÚC:')}")
    print(f"  ├─ Server:      FastAPI + Uvicorn (1 worker, 1 process)")
    print(f"  ├─ ML Inference: Synchronous (blocking event loop)")
    print(f"  ├─ Database:    SQLite (single writer)")
    print(f"  └─ Device:      CPU (no GPU)")

    print(f"\n  {bold('KHẢ NĂNG CHỊU TẢI:')}")

    if max_stable > 0:
        print(f"  ├─ {green('STABLE')}   (≥99% success): {bold(str(max_stable))} concurrent users")
    else:
        print(f"  ├─ {red('STABLE')}   (≥99% success): không đạt ngay cả 1 user")

    if max_degraded > 0:
        print(f"  ├─ {yellow('DEGRADED')} (80-99% success): {bold(str(max_degraded))} concurrent users")
    else:
        print(f"  ├─ {yellow('DEGRADED')} (80-99% success): không có")

    if ml_broken:
        print(f"  └─ {red('BROKEN')}   (<80% success):  từ {bold(str(ml_broken[0].concurrency))} users trở lên")
    else:
        print(f"  └─ {green('BROKEN')}   (<80% success):  không xảy ra trong test range")

    # Latency info
    if ml_ok:
        baseline = ml_ok[0]
        print(f"\n  {bold('LATENCY (baseline 1 user):')}")
        print(f"  ├─ Avg: {ms_color(baseline.avg_ms)}")
        print(f"  ├─ P95: {ms_color(baseline.p95_ms)}")
        print(f"  └─ Max: {ms_color(baseline.max_ms)}")

    # Recommendation
    print(f"\n  {bold('KHUYẾN NGHỊ:')}")

    if max_stable <= 2:
        print(f"  {red('⚠  CRITICAL')}: ML inference đang block event loop!")
        print(f"     → Wrap inference trong asyncio.run_in_executor() để unblock")
        print(f"     → Hoặc chạy nhiều workers: uvicorn --workers 4")
        print(f"     → Hiện tại chỉ phù hợp cho demo/development (~{max(max_stable,1)}-{max_degraded or 2} users)")
    elif max_stable <= 10:
        print(f"  {yellow('⚠  WARNING')}: Hệ thống chịu được {max_stable} users ổn định")
        print(f"     → Tăng workers: uvicorn --workers 4 để scale lên ~{max_stable * 4} users")
        print(f"     → Dùng GPU inference để giảm latency từ {ml_ok[-1].avg_ms:.0f}ms → ~100ms")
    else:
        print(f"  {green('✓  GOOD')}: Hệ thống chịu được {max_stable} concurrent users")
        print(f"     → Scale thêm bằng cách tăng số workers hoặc dùng GPU")

    print(f"\n  {bold('ĐỂ TĂNG CAPACITY:')}")
    print(f"  1. Async ML:   await loop.run_in_executor(None, ml_service.predict, code, model)")
    print(f"  2. Multiworker: uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000")
    print(f"  3. GPU:        Dùng máy có CUDA → tăng throughput ~10x")
    print(f"  4. Queue:      Celery + Redis để xử lý background tasks")
    print(f"  5. Cache:      Redis cache kết quả phân tích trùng lặp")

    print()


def print_errors(ml_results: List[LevelResult]):
    errors_found = False
    for r in ml_results:
        error_types = {}
        for req in r.results:
            if not req.success:
                key = req.error or f"HTTP {req.status_code}"
                error_types[key] = error_types.get(key, 0) + 1
        if error_types:
            if not errors_found:
                print_section("Lỗi phát sinh")
                errors_found = True
            print(f"  │  [{r.concurrency} users] ", end="")
            for err, cnt in error_types.items():
                print(f"{red(err)} x{cnt}  ", end="")
            print()


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────
async def main(base_url: str, max_users: int):
    print_header(f"T07GPTcodeDetect — Load Test  [{datetime.now().strftime('%H:%M:%S')}]")
    print(f"  Target: {cyan(base_url)}")
    print(f"  Requests/level: {REQUESTS_PER_LEVEL}  |  Timeout: {TIMEOUT_SEC}s/request")
    print(f"  Concurrency levels: {CONCURRENCY_LEVELS}")

    # 1. Warm-up
    ok = await warmup(base_url)
    if not ok:
        sys.exit(1)

    # 2. Baseline
    _, baseline_ml = await measure_baseline(base_url)

    # 3. Determine levels to test
    levels = [c for c in CONCURRENCY_LEVELS if c <= max_users]

    # 4. Health endpoint test
    health_results = await run_health_test(base_url, levels)
    print_results_table(health_results, "/health endpoint")

    # 5. ML Analysis test
    ml_results = await run_analysis_test(base_url, levels)
    print_results_table(ml_results, "/api/analysis endpoint (ML)")

    # 6. Error report
    print_errors(ml_results)

    # 7. Summary
    print_summary(health_results, ml_results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T07GPTcodeDetect Load Test")
    parser.add_argument("--url", default=BASE_URL, help="Server URL")
    parser.add_argument("--max-users", type=int, default=50, help="Max concurrent users to test")
    args = parser.parse_args()

    CONCURRENCY_LEVELS_FILTERED = [c for c in CONCURRENCY_LEVELS if c <= args.max_users]

    asyncio.run(main(args.url, args.max_users))
