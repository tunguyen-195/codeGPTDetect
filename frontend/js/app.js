/**
 * T07GPTcodeDetect v3.0 - Frontend Application
 * Hệ thống phát hiện code được sinh bởi các mô hình ngôn ngữ lớn T07
 * Alpine.js-based Single Page Application
 * 
 * Features:
 * - User authentication (register, login, logout)
 * - Code analysis with ML models
 * - Analysis history tracking
 * - User dashboard with statistics
 * - Modern, responsive UI
 */

// Configure axios defaults
axios.defaults.baseURL = window.location.origin;
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Axios interceptor for auth token
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

// Axios interceptor for handling 401 errors
axios.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            // Token expired or invalid - DON'T auto-clear, let the app handle it
            console.log('401 error from:', error.config?.url);
            // Only clear and redirect if it's the auth/me endpoint (session truly expired)
            if (error.config?.url?.includes('/api/auth/me')) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_info');
                if (window.location.pathname !== '/') {
                    window.location.href = '/';
                }
            }
        }
        return Promise.reject(error);
    }
);

/**
 * Main Alpine.js application
 */
function app() {
    return {
        // ========== STATE ==========
        loading: true,
        isLoggedIn: false,
        user: null,
        currentPage: 'dashboard',

        // UI State
        showLogin: false,
        showRegister: false,
        loggingIn: false,
        registering: false,
        analyzing: false,
        loadingHistory: false,
        loadingStats: false,

        // Forms
        loginForm: {
            email: '',
            password: ''
        },

        registerForm: {
            email: '',
            username: '',
            password: '',
            full_name: ''
        },

        analysisForm: {
            code: '',
            language: 'auto',
            model: 'auto',
            save_to_history: true,
            filename: '',
            notes: '',
            tags: []
        },

        // Data
        analysisResult: null,
        history: [],
        stats: {
            total_analyses: 0,
            ai_generated: 0,
            human_written: 0,
            avg_confidence: 0
        },
        availableModels: [],

        // Errors
        loginError: null,
        registerError: null,
        analysisError: null,

        // ========== INITIALIZATION ==========
        async init() {
            console.log('🚀 T07GPTcodeDetect v3.0 initializing...');

            try {
                // Load available models
                await this.loadModels();

                // Check authentication
                await this.checkAuth();

                console.log('✅ Initialization complete');
                console.log('User logged in:', this.isLoggedIn);

            } catch (error) {
                console.error('Initialization error:', error);
            } finally {
                this.loading = false;
            }
        },

        // ========== AUTHENTICATION ==========
        async checkAuth() {
            const token = localStorage.getItem('access_token');
            if (!token) {
                this.isLoggedIn = false;
                return;
            }

            try {
                const response = await axios.get('/api/auth/me');
                this.user = response.data;
                this.isLoggedIn = true;

                console.log('✅ User authenticated:', this.user.username);

                // Load dashboard data
                await this.loadDashboardData();

            } catch (error) {
                console.error('Auth check failed:', error);
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                this.isLoggedIn = false;
            }
        },

        async login() {
            this.loggingIn = true;
            this.loginError = null;

            try {
                const response = await axios.post('/api/auth/login', this.loginForm);

                // Save tokens
                localStorage.setItem('access_token', response.data.access_token);
                localStorage.setItem('refresh_token', response.data.refresh_token);

                // Save user info (including role) for admin panel
                localStorage.setItem('user_info', JSON.stringify(response.data.user));

                // Update state
                this.user = response.data.user;
                this.isLoggedIn = true;
                this.showLogin = false;

                // Reset form
                this.loginForm = { email: '', password: '' };

                // Load dashboard data
                await this.loadDashboardData();

                console.log('✅ Login successful, user:', this.user);

            } catch (error) {
                console.error('Login failed:', error);
                this.loginError = error.response?.data?.detail || 'Login failed. Please check your credentials.';
            } finally {
                this.loggingIn = false;
            }
        },

        async register() {
            this.registering = true;
            this.registerError = null;

            try {
                await axios.post('/api/auth/register', this.registerForm);

                // Auto-login after registration
                this.loginForm.email = this.registerForm.email;
                this.loginForm.password = this.registerForm.password;

                this.showRegister = false;
                this.showLogin = false;

                // Reset register form
                this.registerForm = {
                    email: '',
                    username: '',
                    password: '',
                    full_name: ''
                };

                // Auto-login
                await this.login();

                console.log('✅ Registration successful');

            } catch (error) {
                console.error('Registration failed:', error);
                const detail = error.response?.data?.detail;
                if (typeof detail === 'string') {
                    this.registerError = detail;
                } else if (Array.isArray(detail)) {
                    this.registerError = detail.map(e => e.msg).join(', ');
                } else {
                    this.registerError = 'Registration failed. Please try again.';
                }
            } finally {
                this.registering = false;
            }
        },

        async logout() {
            try {
                await axios.post('/api/auth/logout');
            } catch (error) {
                console.error('Logout request failed:', error);
            } finally {
                // Clear local state
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                this.isLoggedIn = false;
                this.user = null;
                this.history = [];
                this.stats = {
                    total_analyses: 0,
                    ai_generated: 0,
                    human_written: 0,
                    avg_confidence: 0
                };
                this.analysisResult = null;
                console.log('✅ Logged out');
            }
        },

        // ========== MODELS ==========
        async loadModels() {
            try {
                const response = await axios.get('/api/analysis/models');
                this.availableModels = response.data.data.models || [];
                console.log('✅ Models loaded:', this.availableModels);
            } catch (error) {
                console.error('Failed to load models:', error);
                this.availableModels = ['python', 'java', 'base'];
            }
        },

        // ========== CODE ANALYSIS ==========
        async analyzeCode() {
            if (!this.analysisForm.code.trim()) {
                alert('Please enter code to analyze');
                return;
            }

            this.analyzing = true;
            this.analysisError = null;
            this.analysisResult = null;

            try {
                const payload = {
                    code: this.analysisForm.code,
                    language: this.analysisForm.language === 'auto' ? null : this.analysisForm.language,
                    model: this.analysisForm.model === 'auto' ? null : this.analysisForm.model,
                    save_to_history: this.analysisForm.save_to_history && this.isLoggedIn,
                    filename: this.analysisForm.filename || null,
                    notes: this.analysisForm.notes || null,
                    tags: this.analysisForm.tags.length > 0 ? this.analysisForm.tags : null
                };

                const response = await axios.post('/api/analysis', payload);

                this.analysisResult = response.data;

                // Refresh history if saved
                if (this.analysisForm.save_to_history && this.isLoggedIn) {
                    await this.loadHistory();
                    await this.loadStats();
                }

                console.log('✅ Analysis complete:', this.analysisResult);

                // Scroll to results
                setTimeout(() => {
                    document.querySelector('.analysis-results')?.scrollIntoView({ behavior: 'smooth' });
                }, 100);

            } catch (error) {
                console.error('Analysis failed:', error);
                this.analysisError = error.response?.data?.detail || 'Analysis failed. Please try again.';
                alert('Analysis failed: ' + this.analysisError);
            } finally {
                this.analyzing = false;
            }
        },

        clearCode() {
            this.analysisForm.code = '';
            this.analysisResult = null;
            this.analysisError = null;
            this.analysisForm.filename = '';
            this.analysisForm.notes = '';
            this.analysisForm.tags = [];
        },

        loadSampleCode() {
            const samples = {
                python: `def fibonacci(n):
    """Calculate Fibonacci number using recursion"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")`,
                java: `public class Fibonacci {
    public static int fibonacci(int n) {
        if (n <= 1) {
            return n;
        }
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            System.out.println("F(" + i + ") = " + fibonacci(i));
        }
    }
}`
            };

            const lang = this.analysisForm.language === 'auto' ? 'python' : this.analysisForm.language;
            this.analysisForm.code = samples[lang] || samples.python;
        },

        // ========== DASHBOARD DATA ==========
        async loadDashboardData() {
            if (!this.isLoggedIn) return;

            await Promise.all([
                this.loadStats(),
                this.loadHistory()
            ]);
        },

        async loadStats() {
            if (!this.isLoggedIn) return;

            this.loadingStats = true;
            try {
                const response = await axios.get('/api/history/stats');
                this.stats = response.data.data || {};
                console.log('📊 Stats loaded:', this.stats);
            } catch (error) {
                console.error('Failed to load stats:', error);
            } finally {
                this.loadingStats = false;
            }
        },

        async loadHistory() {
            if (!this.isLoggedIn) return;

            this.loadingHistory = true;
            try {
                const response = await axios.get('/api/history?limit=10');
                this.history = response.data.data?.items || [];
                console.log('📜 History loaded:', this.history.length, 'items');
            } catch (error) {
                console.error('Failed to load history:', error);
                this.history = [];
            } finally {
                this.loadingHistory = false;
            }
        },

        async deleteHistory(id) {
            if (!confirm('Delete this analysis from history?')) return;

            try {
                await axios.delete(`/api/history/${id}`);

                // Refresh history and stats
                await this.loadHistory();
                await this.loadStats();

                console.log('✅ History item deleted');

            } catch (error) {
                console.error('Failed to delete history:', error);
                alert('Failed to delete. Please try again.');
            }
        },

        viewHistoryDetails(item) {
            // Load the code into the analysis form
            this.analysisForm.code = item.code;
            this.analysisForm.language = item.language;
            this.analysisForm.model = item.model_used;

            // Show the result
            this.analysisResult = {
                prediction: item.prediction,
                confidence: item.confidence,
                probabilities: item.probabilities,
                language: item.language,
                model_used: item.model_used,
                execution_time: item.execution_time
            };

            // Scroll to analysis section
            setTimeout(() => {
                document.querySelector('.analysis-section')?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
        },

        // ========== UTILITIES ==========
        getToken() {
            return localStorage.getItem('access_token');
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

        formatConfidence(confidence) {
            return (confidence * 100).toFixed(2) + '%';
        },

        getResultClass(prediction) {
            return prediction === 'AI-Generated'
                ? 'border-purple-500 bg-purple-50'
                : 'border-green-500 bg-green-50';
        },

        getResultIcon(prediction) {
            return prediction === 'AI-Generated' ? '🤖' : '✍️';
        },

        getResultText(prediction) {
            return prediction === 'AI-Generated' ? 'AI-Generated' : 'Human-Written';
        },

        getResultColor(prediction) {
            return prediction === 'AI-Generated' ? 'text-purple-600' : 'text-green-600';
        },

        // ========== MODAL CONTROLS ==========
        openLogin() {
            this.showLogin = true;
            this.showRegister = false;
            this.loginError = null;
        },

        openRegister() {
            this.showRegister = true;
            this.showLogin = false;
            this.registerError = null;
        },

        closeModals() {
            this.showLogin = false;
            this.showRegister = false;
            this.loginError = null;
            this.registerError = null;
        }
    }
}

// Initialize on page load
console.log('📦 T07GPTcodeDetect v3.0 - App script loaded');
console.log('Alpine.js version:', window.Alpine?.version || 'loading...');
