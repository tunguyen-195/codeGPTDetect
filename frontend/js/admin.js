/**
 * T07GPTcodeDetect v3.0 - Admin Panel Application
 * Alpine.js-based Admin Dashboard
 */

// Configure axios
axios.defaults.baseURL = window.location.origin;
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Auth interceptor
axios.interceptors.request.use(
    config => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

// 401 handler - DON'T auto-redirect, let the app handle it
axios.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            console.log('401 Unauthorized - request failed:', error.config?.url);
            // Don't auto-redirect, let checkAdminAccess handle it
        }
        return Promise.reject(error);
    }
);

/**
 * Admin Panel Alpine.js Application
 */
function adminApp() {
    return {
        // State
        loading: true,
        accessDenied: false,
        deniedReason: '',
        user: null,
        currentTab: 'dashboard',

        // Data
        stats: {},
        recentUsers: [],
        recentAnalyses: [],
        users: [],
        allAnalyses: [],
        health: {},

        // Charts
        languageChart: null,
        predictionChart: null,

        // ========== INITIALIZATION ==========
        async init() {
            console.log('🔐 Admin Panel initializing...');
            console.log('Token in localStorage:', localStorage.getItem('access_token') ? 'EXISTS' : 'NOT FOUND');

            try {
                // Check if user is logged in and is admin
                await this.checkAdminAccess();

                if (!this.accessDenied) {
                    // Load dashboard data
                    await this.loadDashboardData();

                    // Initialize charts after a short delay
                    setTimeout(() => this.initCharts(), 100);
                }

            } catch (error) {
                console.error('Admin init error:', error);
                this.accessDenied = true;
                this.deniedReason = 'Lỗi khởi tạo: ' + error.message;
            } finally {
                this.loading = false;
            }
        },

        async checkAdminAccess() {
            const token = localStorage.getItem('access_token');
            if (!token) {
                console.log('No token found');
                this.accessDenied = true;
                this.deniedReason = 'Bạn chưa đăng nhập. Vui lòng đăng nhập trước.';
                return;
            }

            try {
                // Try to get user info from localStorage first (saved during login)
                const userInfoStr = localStorage.getItem('user_info');
                if (userInfoStr) {
                    this.user = JSON.parse(userInfoStr);
                    console.log('User info from localStorage:', this.user);
                } else {
                    // Fallback to API call
                    console.log('No user_info in localStorage, calling API...');
                    const response = await axios.get('/api/auth/me');
                    console.log('API /api/auth/me response:', response.data);
                    this.user = response.data;
                    // Save for future use
                    localStorage.setItem('user_info', JSON.stringify(this.user));
                }

                // Check if user is admin
                console.log('User role:', this.user.role);
                if (this.user.role !== 'admin') {
                    console.log('User is not admin:', this.user.role);
                    this.accessDenied = true;
                    this.deniedReason = `Role hiện tại: "${this.user.role}". Cần role "admin".`;
                    return;
                }

                console.log('✅ Admin access granted:', this.user.username);

            } catch (error) {
                console.error('Auth check failed:', error);
                this.accessDenied = true;
                this.deniedReason = 'Không thể xác thực. Vui lòng đăng nhập lại.';
            }
        },

        // ========== DATA LOADING ==========
        async loadDashboardData() {
            await Promise.all([
                this.loadStats(),
                this.loadRecentUsers(),
                this.loadRecentAnalyses(),
                this.checkHealth()
            ]);
        },

        async loadStats() {
            try {
                const response = await axios.get('/api/admin/stats');
                this.stats = response.data.data || {};
                console.log('📊 Stats loaded:', this.stats);
            } catch (error) {
                console.error('Failed to load stats:', error);
            }
        },

        async loadRecentUsers() {
            try {
                const response = await axios.get('/api/admin/users/recent?limit=5');
                this.recentUsers = response.data.data?.users || [];
                console.log('👥 Recent users loaded:', this.recentUsers.length);
            } catch (error) {
                console.error('Failed to load recent users:', error);
            }
        },

        async loadRecentAnalyses() {
            try {
                const response = await axios.get('/api/admin/analyses/recent?limit=5');
                this.recentAnalyses = response.data.data?.analyses || [];
                console.log('📜 Recent analyses loaded:', this.recentAnalyses.length);
            } catch (error) {
                console.error('Failed to load recent analyses:', error);
            }
        },

        async loadUsers() {
            try {
                const response = await axios.get('/api/users');
                this.users = response.data.data?.items || [];
                console.log('👥 All users loaded:', this.users.length);
            } catch (error) {
                console.error('Failed to load users:', error);
                alert('Không thể tải danh sách users');
            }
        },

        async loadAllAnalyses() {
            try {
                const response = await axios.get('/api/admin/analyses/recent?limit=50');
                this.allAnalyses = response.data.data?.analyses || [];
                console.log('📜 All analyses loaded:', this.allAnalyses.length);
            } catch (error) {
                console.error('Failed to load analyses:', error);
            }
        },

        async checkHealth() {
            try {
                const response = await axios.get('/api/admin/health');
                this.health = response.data.data || {};
                console.log('💚 Health check:', this.health);
            } catch (error) {
                console.error('Health check failed:', error);
                this.health = { status: 'error', database: 'unknown' };
            }
        },

        // ========== USER MANAGEMENT ==========
        async updateRole(userId, newRole) {
            try {
                await axios.patch(`/api/users/${userId}/role?new_role=${newRole}`);
                console.log('✅ Role updated:', userId, newRole);
                await this.loadUsers();
            } catch (error) {
                console.error('Failed to update role:', error);
                alert('Không thể cập nhật role');
                await this.loadUsers(); // Reload to reset
            }
        },

        async toggleStatus(userId, currentStatus) {
            try {
                await axios.patch(`/api/users/${userId}/status?is_active=${!currentStatus}`);
                console.log('✅ Status toggled:', userId);
                await this.loadUsers();
            } catch (error) {
                console.error('Failed to toggle status:', error);
                alert('Không thể thay đổi trạng thái');
            }
        },

        async deleteUser(userId, username) {
            if (!confirm(`Xác nhận xóa user "${username}"?`)) return;

            try {
                await axios.delete(`/api/users/${userId}`);
                console.log('✅ User deleted:', userId);
                await this.loadUsers();
                await this.loadStats();
            } catch (error) {
                console.error('Failed to delete user:', error);
                alert('Không thể xóa user: ' + (error.response?.data?.detail || 'Unknown error'));
            }
        },

        // ========== CHARTS ==========
        initCharts() {
            this.initLanguageChart();
            this.initPredictionChart();
        },

        initLanguageChart() {
            const ctx = document.getElementById('languageChart');
            if (!ctx) return;

            const byLanguage = this.stats.analyses?.by_language || {};
            const labels = Object.keys(byLanguage);
            const data = Object.values(byLanguage);

            if (this.languageChart) {
                this.languageChart.destroy();
            }

            this.languageChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels.length > 0 ? labels : ['No data'],
                    datasets: [{
                        data: data.length > 0 ? data : [1],
                        backgroundColor: [
                            '#8B5CF6',
                            '#10B981',
                            '#F59E0B',
                            '#EF4444',
                            '#3B82F6'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        },

        initPredictionChart() {
            const ctx = document.getElementById('predictionChart');
            if (!ctx) return;

            const aiCount = this.stats.analyses?.ai_generated || 0;
            const humanCount = this.stats.analyses?.human_written || 0;

            if (this.predictionChart) {
                this.predictionChart.destroy();
            }

            this.predictionChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['AI-Generated', 'Human-Written'],
                    datasets: [{
                        data: [aiCount, humanCount],
                        backgroundColor: ['#8B5CF6', '#10B981']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        },

        // ========== UTILITIES ==========
        getTabTitle() {
            const titles = {
                'dashboard': '📊 Dashboard',
                'users': '👥 Quản Lý Users',
                'history': '📜 Lịch Sử Phân Tích',
                'system': '⚙️ System Health'
            };
            return titles[this.currentTab] || 'Dashboard';
        },

        formatDate(dateString) {
            if (!dateString) return 'N/A';
            const date = new Date(dateString);
            return date.toLocaleString('vi-VN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
        },

        async logout() {
            try {
                await axios.post('/api/auth/logout');
            } catch (error) {
                console.error('Logout error:', error);
            } finally {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/';
            }
        },

        // Watch for tab changes to load data
        $watch: {
            currentTab(newTab) {
                if (newTab === 'users' && this.users.length === 0) {
                    this.loadUsers();
                }
                if (newTab === 'history' && this.allAnalyses.length === 0) {
                    this.loadAllAnalyses();
                }
            }
        }
    }
}

// Tab watcher workaround for Alpine.js
document.addEventListener('alpine:init', () => {
    Alpine.effect(() => {
        const app = Alpine.store('adminApp');
        if (app) {
            // This will be called when currentTab changes
        }
    });
});

console.log('📦 Admin Panel script loaded');
