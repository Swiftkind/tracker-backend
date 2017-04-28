/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

	__webpack_require__(1);
	__webpack_require__(2);
	__webpack_require__(4);
	module.exports = __webpack_require__(3);


/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

	'use strict';

	var _componentsControllersEs6 = __webpack_require__(2);

	var _componentsServicesEs6 = __webpack_require__(3);

	angular.module('tracker', ['ui.router', 'ui.bootstrap', 'angularMoment', 'angular-storage', 'angular-jwt', 'angular-duration-format', 'timer', 'ngFileUpload', 'angular.filter', 'ui.select', 'ngSanitize', 'sc.select', 'ui-notification', 'obDateRangePicker']).constant('TEMPLATE_URL', 'static/app/templates/').constant('API_URL', 'http://127.0.0.1:8080/api/').service('AccountService', _componentsServicesEs6.AccountService).service('AuthService', _componentsServicesEs6.AuthService).service('AdminService', _componentsServicesEs6.AdminService).controller('DashboardController', _componentsControllersEs6.DashboardController).controller('AccountSettingController', _componentsControllersEs6.AccountSettingController).controller('SignupController', _componentsControllersEs6.SignupController).controller('LoginController', _componentsControllersEs6.LoginController).controller('AdminDashboardController', _componentsControllersEs6.AdminDashboardController).controller('UpdateLogController', _componentsControllersEs6.UpdateLogController).filter('toHrs', function () {
	    return function (input) {
	        var total = 0;
	        for (var i = 0; i < input.length; i++) {
	            var log = input[i];
	            total += log * 1000;
	        }
	        return total;
	    };
	});

/***/ }),
/* 2 */
/***/ (function(module, exports) {

	'use strict';

	Object.defineProperty(exports, '__esModule', {
	    value: true
	});

	var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }

	var DashboardController = (function () {
	    function DashboardController($scope, $state, $window, $rootScope, $uibModal, moment, AccountService, AuthService) {

	        'ngInject';

	        var _this = this;

	        _classCallCheck(this, DashboardController);

	        this._$uibModal = $uibModal;
	        this._$moment = moment;
	        this.$rootScope = $rootScope;
	        this.$rootScope.$on('$stateChangeStart', this.activeDashboard());
	        this.AccountService = AccountService;

	        $scope.tracking = false;
	        $scope.reloaded = true;
	        $scope.ongoing = false;
	        $scope.stopped = false;
	        $scope.logs = [];
	        $scope.projects = [];
	        $scope.project = undefined;
	        $scope.user = undefined;

	        $scope.logout = function () {
	            AuthService.logout();
	        };

	        /// get current user data
	        $scope.$watch(function () {
	            return AccountService.loaded;
	        }, function (isReady) {
	            if (!isReady) {
	                $scope.user = AccountService.user;
	                $scope.user.birthdate = moment(AccountService.user.birthdate).toDate();
	            }
	        });

	        ///get all projects of authenticated user
	        AccountService.getProjects().then(function (resp) {
	            var data = resp.data;

	            $scope.projects = data;
	            if (data.length > 0) {
	                $scope.selectedProject = data[0];
	                $scope.currentProject = data[0];
	            }
	        });

	        ///get all user's logs
	        ($scope.completeLogs = function () {
	            AccountService.getAllLogs().then(function (resp) {
	                $scope.allLogs = resp.data;
	                var project = $scope.selectedProject;

	                var allLogs = [];
	                $scope.allLogs.map(function (log) {
	                    if (log.project == project.id) {
	                        return allLogs.push(log);
	                    }
	                });
	                $scope.logs = allLogs.slice(0);
	            });
	        })();

	        ///get current running log (if available)
	        AccountService.getCurrentLog().then(function (resp) {
	            var data = resp.data;
	            if (data.project != null) {
	                $scope.selectedLog = $scope.currentLog = data;
	                $scope.ongoing = true;

	                var date = _this._$moment(data.start).toDate();
	                $scope.started = date.getTime();

	                $scope.projects.find(function (project) {
	                    if (project.id == data.project) {
	                        return $scope.selectedProject = project;
	                    }
	                });
	            }
	            $scope.tracking = data.project != null;
	        });

	        ///EVENT FUNCTIONS
	        $scope.selectLog = function (logs) {
	            var log = logs.slice(-1)[0];
	            $scope.selectedLog = log;
	        };

	        $scope.viewProjectLogs = function (project) {
	            $scope.selectedProject = project;
	            $scope.logs = [];
	            $scope.allLogs.map(function (log) {
	                if (log.project == project.id) {
	                    return $scope.logs.push(log);
	                }
	            });
	        };

	        $scope.createNewLog = function (newLog) {
	            var data = {
	                "project": $scope.selectedProject.id,
	                "memo": newLog.memo,
	                "timein": true
	            };
	            AccountService.playTracker(data).then(function (resp) {
	                var data = resp.data;
	                $scope.currentLog = data;
	                $scope.logs.push(data);
	                $scope.selectedLog = data;
	                $scope.tracking = true;
	                $scope.reloaded = false;
	                $scope.newLog.memo = '';
	            })['catch'](function (err) {
	                console.log(err);
	            });
	            setTimeout(function () {
	                $scope.$broadcast('timer-start');
	            }, 500);
	        };

	        $scope.startTracker = function (selectedLog) {
	            $scope.started = new Date().getTime();
	            var data = {
	                "project": selectedLog.project,
	                "memo": selectedLog.memo,
	                "timein": true
	            };

	            AccountService.playTracker(data).then(function (resp) {
	                $scope.currentLog = resp.data;
	                $scope.tracking = true;
	                $scope.reloaded = false;
	            })['catch'](function (err) {
	                console.log(err);
	            });
	            setTimeout(function () {
	                $scope.$broadcast('timer-start');
	            }, 500);
	        };

	        $scope.stopTracker = function (selectedLog) {
	            var data = {
	                "project": selectedLog.project,
	                "memo": selectedLog.memo,
	                "timein": false
	            };
	            AccountService.playTracker(data).then(function (resp) {
	                $scope.tracking = false;
	                $scope.ongoing = false;
	                $scope.completeLogs();
	                if ($scope.reloaded) {
	                    $scope.stopped = true;
	                }
	            })['catch'](function (err) {
	                console.log(err);
	            });
	            setTimeout(function () {
	                $scope.$broadcast('timer-stop');
	            }, 500);
	        };

	        //LOGS FILTERING
	        $scope.getLogs = function (project_id) {
	            var key = $scope.logsKey;
	            var currDate = new Date();

	            if (project_id) {
	                $scope.logs = [];
	                $scope.allLogs.map(function (log) {
	                    if (log.project == project_id) {
	                        return $scope.logs.push(log);
	                    }
	                });
	            };
	            if (key == 'today') {
	                (function () {
	                    var today = currDate.getDate();
	                    var currentLogs = $scope.logs;

	                    $scope.logs = currentLogs.filter(function (log) {
	                        var date = _this._$moment(log.start).toDate().getDate();
	                        if (today == date) {
	                            return log;
	                        }
	                    });
	                })();
	            } else if (key == 'yesterday') {
	                (function () {
	                    var yesterday = currDate.getDate() - 1;
	                    var currentLogs = $scope.logs;

	                    $scope.logs = currentLogs.filter(function (log) {
	                        var date = _this._$moment(log.start).toDate().getDate();
	                        if (yesterday == date) {
	                            return log;
	                        }
	                    });
	                })();
	            } else if (key == 'week') {
	                (function () {
	                    var currentLogs = $scope.logs;
	                    // First day of the week
	                    var firstday = currDate.getDate() - currDate.getDay();
	                    // Last day of the week
	                    var lastday = firstday + 6;

	                    $scope.logs = currentLogs.filter(function (log) {
	                        var date = _this._$moment(log.start).toDate().getDate();
	                        if (date >= firstday && date <= lastday) {
	                            return log;
	                        }
	                    });
	                })();
	            } else if (key == 'month') {
	                (function () {
	                    var currentLogs = $scope.logs;
	                    // First day of the month
	                    var firstday = new Date(currDate.getFullYear(), currDate.getMonth(), 1).getDate();
	                    // Last day of the month
	                    var lastday = new Date(currDate.getFullYear(), currDate.getMonth() + 1, 0).getDate();

	                    $scope.logs = currentLogs.filter(function (log) {
	                        var date = _this._$moment(log.start).toDate().getDate();
	                        if (date >= firstday && date <= lastday) {
	                            return log;
	                        }
	                    });
	                })();
	            } else if (key == 'approved') {
	                var currentLogs = $scope.logs;

	                $scope.logs = currentLogs.filter(function (log) {
	                    if (log.is_approved == true) {
	                        return log;
	                    }
	                });
	            } else {
	                return $scope.logs;
	            }
	        };

	        $scope.$watch(function () {
	            if ($scope.tracking) {
	                $window.onbeforeunload = function (event) {
	                    return "Tracker still running!";
	                };
	            };
	        });

	        //MODAL
	        $scope.openAccountSetting = function () {
	            var modalInstance = _this._$uibModal.open({
	                windowTemplateUrl: 'static/node_modules/angular-ui-bootstrap/template/modal/window.html',
	                animation: true,
	                backdrop: 'static',
	                keyboard: false,
	                templateUrl: 'account-setting.html',
	                controller: 'AccountSettingController',
	                controllerAs: 'ctrl',
	                scope: $scope
	            });
	        };

	        $scope.openUpdateLog = function (log) {
	            $scope.selectedLog = log;

	            var modalInstance = _this._$uibModal.open({
	                windowTemplateUrl: 'static/node_modules/angular-ui-bootstrap/template/modal/window.html',
	                animation: true,
	                backdrop: 'static',
	                keyboard: false,
	                templateUrl: 'update-log.html',
	                controller: 'UpdateLogController',
	                controllerAs: 'ctrl',
	                scope: $scope,
	                resolve: {
	                    log: function log() {
	                        return $scope.selectedLog;
	                    }
	                }
	            });
	        };
	    }

	    //ACCOUNT SETTING CONTROLLER

	    _createClass(DashboardController, [{
	        key: 'activeDashboard',
	        value: function activeDashboard() {
	            var bodyClass = document.getElementById("main-body").classList;

	            bodyClass.add('left-open', 'right-open');
	            return function (event, toState, toParams) {
	                bodyClass.remove('left-open', 'right-open');
	            };
	        }
	    }]);

	    return DashboardController;
	})();

	var AccountSettingController = function AccountSettingController($scope, $uibModalInstance, moment, AccountService, AuthService) {
	    'ngInject';

	    var _this2 = this;

	    _classCallCheck(this, AccountSettingController);

	    this._$uibModalInstance = $uibModalInstance;
	    $scope.uploadSuccess = false;
	    $scope.errors;

	    $scope.updateProfile = function (form) {
	        var data = angular.copy(form);
	        data.birthdate = moment(data.birthdate).format('YYYY-MM-DD');

	        AccountService.update(data).then(function (resp) {
	            _this2._$uibModalInstance.close();
	        })['catch'](function (error) {
	            $scope.errors = error.data;
	        });
	    };

	    $scope.uploadPhoto = function (form) {
	        AccountService.uploadPhoto(form).then(function (resp) {
	            $scope.uploadSuccess = true;
	            $scope.user.profile_photo = resp.data.profile_photo;
	            $scope.change = false;
	        })['catch'](function (error) {
	            console.log('error');
	        });
	    };

	    //EVENT FUNCTION
	    $scope.cancel = function () {
	        _this2._$uibModalInstance.close();
	        AccountService.getCurrentUser().then(function (account) {
	            $scope.user = account;
	        });
	    };

	    $scope.cancelUpload = function () {
	        AccountService.getCurrentUser().then(function (account) {
	            $scope.user.profile_photo = account.profile_photo;
	            $scope.change = false;
	        });
	    };
	}

	//UPDATE LOG CONTROLLER
	;

	var UpdateLogController = function UpdateLogController($scope, moment, $uibModalInstance, AccountService) {
	    'ngInject';

	    var _this3 = this;

	    _classCallCheck(this, UpdateLogController);

	    this._$uibModalInstance = $uibModalInstance;
	    this._moment = moment;

	    $scope.updateLog = function (log) {
	        var data = angular.copy(log);

	        data.start = _this3._moment(data.start).toDate();
	        data.end = _this3._moment(data.end).toDate();
	        AccountService.updateLog(data).then(function (resp) {
	            $scope.selectedLog = resp.data;
	        })['catch'](function (err) {
	            console.log(err);
	        });
	    };
	    //EVENT FUNCTION
	    $scope.cancel = function () {
	        _this3._$uibModalInstance.close();
	    };
	}

	//USER SIGNUP CONTROLLER
	;

	var SignupController = function SignupController($scope, $state, moment, AccountService) {
	    var _this4 = this;

	    _classCallCheck(this, SignupController);

	    this.moment = moment;
	    this.$state = $state;
	    $scope.form = {
	        'gender': 'm',
	        'position': 'designer'
	    };

	    $scope.signup = function (form) {
	        var data = angular.copy(form);

	        data.birthdate = _this4.moment(data.birthdate).format('YYYY-MM-DD');

	        AccountService.signup(data).then(function (resp) {
	            _this4.$state.go('login');
	        })['catch'](function (err) {
	            console.log(err);
	        });
	    };
	}

	//ADMIN CONTROLLER
	;

	var AdminDashboardController = function AdminDashboardController($scope, $state, AuthService, AccountService, AdminService, store, moment, filterFilter, Notification) {
	    'ngInject';

	    var _this5 = this;

	    _classCallCheck(this, AdminDashboardController);

	    this.$scope = $scope;
	    this.AuthService = AuthService;
	    this.AccountService = AccountService;
	    this.AdminService = AdminService;

	    $scope.user = undefined;
	    $scope.projectMembers = [];
	    $scope.members = [];
	    $scope.projects = [];
	    $scope.allMembers = [];

	    $scope.logout = function () {
	        AuthService.logout();
	    };

	    $scope.$watch(function () {
	        return _this5.AccountService.loaded;
	    }, function (isReady) {
	        if (!isReady) {
	            $scope.user = _this5.AccountService.user;
	        }
	    });

	    ///get all projects of current admin
	    AccountService.getAllProjects().then(function (resp) {
	        $scope.projects = resp.data;
	    });

	    ///get all members on different projects
	    ($scope.allMembers = function () {
	        AccountService.getProjectMembers().then(function (resp) {
	            $scope.projectMembers = resp.data;
	        });
	    })();

	    ///get all accounts
	    ($scope.allAccounts = function () {
	        AccountService.getAccounts().then(function (resp) {
	            $scope.accounts = resp.data;
	        });
	    })();

	    $scope.getMembers = function (project) {
	        $scope.project = project;
	        $scope.members = [];
	        $scope.projectMember = [];
	        $scope.projectMembers.map(function (account) {
	            if (account.project == project.id) {
	                $scope.members.push(account);
	                $scope.selectedMember = account;
	                $scope.selectedProject = project.name;
	                $scope.currentProject = project;
	                $scope.projectMember.push(account);
	            }
	        });
	        AccountService.getProjectNoneMembers($scope.members).then(function (resp) {
	            $scope.filteredMembers = resp.data;
	        });
	    };

	    $scope.inviteMember = function (project) {
	        if (!project.member) {
	            Notification.clearAll();
	            Notification.warning('No email inputted!');
	        } else {
	            Notification.info('Sending...');
	            AccountService.sendInvite(project).then(function (resp) {
	                Notification.clearAll();
	                Notification.success('Invitation Sent!');
	                $scope.project.member = '';
	                $scope.members.push(resp.data);
	            })['catch'](function (err) {
	                if (err.status == 500) {
	                    Notification.clearAll();
	                    Notification.warning({ message: 'Make sure that this email was not added yet to this project.', title: 'Failed:' });
	                };
	                console.log(err.data);
	            });
	        };
	    };

	    //get all projects
	    this.AdminService.getProjects().then(function (resp) {
	        var data = resp;
	        $scope.currentProject = undefined;
	        $scope.projects = data;
	        if (data.length > 0) {
	            return $scope.currentProject = data[0];
	        }
	    });

	    this.AdminService.getMembers().then(function (resp) {
	        var data = resp;
	        $scope.allMembers = data;

	        //set current project
	        $scope.projectMember = [];
	        data.map(function (member) {
	            var project = $scope.currentProject;
	            if (member.project == project.id) {
	                $scope.selectedMember = member;
	                $scope.selectedProject = project.name;
	                $scope.currentProject = project;
	                return $scope.projectMember.push(member);
	            }
	        });
	    });

	    // get project members
	    $scope.projectMembers = function (project) {
	        $scope.projectMember = [];
	        $scope.allMembers.map(function (member) {
	            if (member.project == project.id) {
	                $scope.selectedMember = member;
	                $scope.selectedProject = project.name;
	                $scope.currentProject = project;
	                return $scope.projectMember.push(member);
	            }
	        });
	    };

	    $scope.allMemberLogs = [];
	    this.AdminService.getMemberLogs().then(function (resp) {
	        $scope.allMemberLogs = resp;
	    });

	    //default date range
	    this.dateStart = moment().startOf('isoweek').format('YYYY-MM-DD');
	    this.dateEnd = moment().endOf('isoweek').format('YYYY-MM-DD');

	    // get member all logs
	    $scope.memberLogs = function (member) {
	        $scope.memberLog = [];
	        $scope.userLog = [];
	        $scope.selectedUser = member;
	        $scope.allMemberLogs.map(function (log) {
	            if (log.member.project == member.project) {
	                if (member.account == log.member.account) {
	                    log.start = moment(log.start).format('YYYY-MM-DD');
	                    log.seconds = moment.duration(log.log_field).asSeconds();
	                    if (_this5.dateStart <= log.start && log.start <= _this5.dateEnd) {
	                        $scope.userLog.push(log.log_field);
	                        return $scope.memberLog.push(log);
	                    }
	                }
	            }
	        });

	        // get total hours
	        var total = 0;
	        $scope.totalHours = 0;
	        for (var i = 0; i < $scope.userLog.length; i++) {
	            var log = $scope.userLog[i];
	            var logSeconds = moment.duration(log).asSeconds();
	            total += logSeconds * 1000;
	        }
	        $scope.totalHours = total;
	    };

	    //date range filter
	    $scope.dateRangeFilter = function (fieldName, minValue, maxValue) {
	        if (!minValue && !maxValue) return;
	        return function (item) {
	            return minValue <= item[fieldName] && item[fieldName] <= maxValue;
	        };
	    };

	    this.dateRangeApi = {};
	    this.dropsUp = false;
	    this.opens = 'center';
	    this.disabled = false;
	    this.format = 'YYYY-MM-DD';
	    this.autoApply = true;
	    this.weekStart = 'mo';
	    this.linked = true;
	    this.calendarsAlwaysOn = true;

	    this.range = {
	        start: moment().startOf('isoweek'),
	        end: moment().endOf('isoweek')
	    };

	    this.setRange = function () {
	        _this5.dateRangeApi.setDateRange({
	            start: moment().startOf('isoweek'),
	            end: moment().endOf('isoweek')
	        });
	    };

	    this.ranges = [{
	        name: 'Today',
	        start: moment(),
	        end: moment()
	    }, {
	        name: 'Yesterday',
	        start: moment().subtract(1, 'd'),
	        end: moment().subtract(1, 'd')
	    }, {
	        name: 'Current Week',
	        start: moment().startOf('isoweek'),
	        end: moment().endOf('isoweek')
	    }, {
	        name: 'Current Month',
	        start: moment().startOf('month'),
	        end: moment()
	    }];

	    this.rangeApplied = function (start, end) {
	        _this5.dateStart = moment(start).format('YYYY-MM-DD');
	        _this5.dateEnd = moment(end).format('YYYY-MM-DD');
	    };
	}

	//LOGIN CONTROLLER
	;

	var LoginController = function LoginController($scope, $state, $window, store, AuthService) {
	    _classCallCheck(this, LoginController);

	    $scope.form = {};
	    $scope.errors = {};

	    $scope.userLogin = function (form) {
	        AuthService.login(form).then(function () {
	            $window.location.reload();
	        })['catch'](function (error) {
	            $scope.errors = error;
	        });
	    };

	    AuthService.getAuthUser().then(function (account) {
	        if (AuthService.isAuthenticated() && $state.current.name === 'login') {
	            if (account.is_admin === true) {
	                store.set('account_type', 'admin');
	                $state.go('admin');
	            } else {
	                store.set('account_type', 'user');
	                $state.go('dashboard');
	            }
	        }
	    });
	};

	exports.DashboardController = DashboardController;
	exports.AccountSettingController = AccountSettingController;
	exports.SignupController = SignupController;
	exports.LoginController = LoginController;
	exports.AdminDashboardController = AdminDashboardController;
	exports.UpdateLogController = UpdateLogController;

/***/ }),
/* 3 */
/***/ (function(module, exports) {

	'use strict';

	Object.defineProperty(exports, '__esModule', {
	    value: true
	});

	var _createClass = (function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ('value' in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; })();

	function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError('Cannot call a class as a function'); } }

	var AccountService = (function () {
	    function AccountService($http, API_URL, Upload) {
	        _classCallCheck(this, AccountService);

	        this._$http = $http;
	        this._API_URL = API_URL;
	        this._Upload = Upload;
	        this.user = undefined;
	        this.loaded = false;
	        this.getCurrentUser();
	    }

	    _createClass(AccountService, [{
	        key: 'signup',
	        value: function signup(form) {
	            return this._$http.post(this._API_URL + 'account/', form);
	        }
	    }, {
	        key: 'update',
	        value: function update(form) {
	            return this._$http.put(this._API_URL + 'account/', form).then(function (resp) {
	                return resp.data;
	            });
	        }
	    }, {
	        key: 'playTracker',
	        value: function playTracker(data) {
	            return this._$http.post(this._API_URL + 'timelog/', data);
	        }
	    }, {
	        key: 'getCurrentLog',
	        value: function getCurrentLog() {
	            return this._$http.get(this._API_URL + 'timelog/');
	        }
	    }, {
	        key: 'updateLog',
	        value: function updateLog(data) {
	            return this._$http.put(this._API_URL + 'timelog/', data);
	        }
	    }, {
	        key: 'getProjects',
	        value: function getProjects() {
	            return this._$http.get(this._API_URL + 'projects/');
	        }
	    }, {
	        key: 'getAllLogs',
	        value: function getAllLogs() {
	            return this._$http.get(this._API_URL + 'logs/');
	        }
	    }, {
	        key: 'update',
	        value: function update(form) {
	            return this._$http.put(this._API_URL + 'account/', form).then(function (resp) {
	                return resp.data;
	            });
	        }
	    }, {
	        key: 'uploadPhoto',
	        value: function uploadPhoto(form) {
	            return this._Upload.upload({
	                url: this._API_URL + 'photo/',
	                data: form,
	                method: 'PUT'
	            });
	        }
	    }, {
	        key: 'getCurrentUser',
	        value: function getCurrentUser() {
	            var _this = this;

	            if (this.loaded) return;
	            this.loaded = true;
	            return this._$http.get(this._API_URL + 'account/').then(function (result) {
	                _this.loaded = false;
	                _this.user = result.data;
	                return result.data;
	            });
	        }
	    }, {
	        key: 'getAllProjects',
	        value: function getAllProjects() {
	            return this._$http.get(this._API_URL + 'project-list/');
	        }
	    }, {
	        key: 'getProjectMembers',
	        value: function getProjectMembers() {
	            return this._$http.get(this._API_URL + 'members/');
	        }
	    }, {
	        key: 'getProjectNoneMembers',
	        value: function getProjectNoneMembers(data) {
	            return this._$http.post(this._API_URL + 'members/', data);
	        }
	    }, {
	        key: 'getAccounts',
	        value: function getAccounts() {
	            return this._$http.get(this._API_URL + 'accounts/');
	        }
	    }, {
	        key: 'sendInvite',
	        value: function sendInvite(data) {
	            return this._$http.post(this._API_URL + 'invite/', data);
	        }
	    }]);

	    return AccountService;
	})();

	var AuthService = (function () {
	    function AuthService($state, $q, $http, $window, $location, API_URL, store) {
	        _classCallCheck(this, AuthService);

	        this.$http = $http;
	        this.$state = $state;
	        this.$location = $location;
	        this.$window = $window;
	        this.$q = $q;
	        this.API_URL = API_URL;
	        this.store = store;
	        this.loaded = false;
	    }

	    _createClass(AuthService, [{
	        key: 'login',
	        value: function login(form) {
	            var _this2 = this;

	            return this.$http.post(this.API_URL + 'token/', form).then(function (resp) {
	                _this2.store.set('token', resp.data.token);
	            })['catch'](function (error) {
	                return _this2.$q.reject(error.data);
	            });
	        }
	    }, {
	        key: 'logout',
	        value: function logout() {
	            var _this3 = this;

	            return this.$http.get(this.API_URL + 'logout/').then(function () {
	                _this3.cleanCredentials();
	            })['catch'](function (error) {
	                return _this3.$q.reject(error.data);
	            });
	        }
	    }, {
	        key: 'getAuthUser',
	        value: function getAuthUser() {
	            return this.$http.get(this.API_URL + 'account/').then(function (result) {
	                return result.data;
	            });
	        }
	    }, {
	        key: 'isAuthenticated',
	        value: function isAuthenticated() {
	            var credentials = undefined;

	            credentials = this.getCredentials();
	            return !!credentials.token;
	        }
	    }, {
	        key: 'cleanCredentials',
	        value: function cleanCredentials() {
	            this.store.remove('token');
	            this.store.remove('account_type');
	        }
	    }, {
	        key: 'getCredentials',
	        value: function getCredentials() {
	            var token = undefined;

	            token = this.store.get('token');
	            return {
	                token: token
	            };
	        }
	    }]);

	    return AuthService;
	})();

	var AdminService = (function () {
	    function AdminService($state, $q, $http, $window, $location, API_URL) {
	        _classCallCheck(this, AdminService);

	        this._$http = $http;
	        this._API_URL = API_URL;
	    }

	    _createClass(AdminService, [{
	        key: 'getProjects',
	        value: function getProjects() {
	            return this._$http.get(this._API_URL + 'project-list/').then(function (result) {
	                return result.data;
	            });
	        }
	    }, {
	        key: 'getMembers',
	        value: function getMembers() {
	            return this._$http.get(this._API_URL + 'members/').then(function (result) {
	                return result.data;
	            });
	        }
	    }, {
	        key: 'getMemberLogs',
	        value: function getMemberLogs() {
	            return this._$http.get(this._API_URL + 'members/logs/').then(function (result) {
	                return result.data;
	            });
	        }
	    }]);

	    return AdminService;
	})();

	exports.AccountService = AccountService;
	exports.AuthService = AuthService;
	exports.AdminService = AdminService;

/***/ }),
/* 4 */
/***/ (function(module, exports) {

	'use strict';

	angular.module('tracker').config(function ($urlMatcherFactoryProvider, $stateProvider, $httpProvider, $urlRouterProvider, $locationProvider, TEMPLATE_URL, API_URL) {
	    'ngInject';
	    $locationProvider.hashPrefix('');
	    $urlRouterProvider.otherwise('/');
	    $urlMatcherFactoryProvider.strictMode(false);
	    $stateProvider.state('legacy', {
	        abstract: true,
	        url: '',
	        template: '<ui-view></ui-view>'
	    }).state('login', {
	        url: '/',
	        templateUrl: TEMPLATE_URL + 'accounts/login.html',
	        controller: 'LoginController',
	        controllerAs: 'ctrl'
	    }).state('signup', {
	        url: '/signup/',
	        templateUrl: TEMPLATE_URL + 'accounts/create.html',
	        controller: 'SignupController',
	        controllerAs: 'ctrl',
	        role: 'anon'
	    }).state('dashboard', {
	        url: '/dashboard/',
	        templateUrl: TEMPLATE_URL + 'accounts/dashboard.html',
	        controller: 'DashboardController',
	        controllerAs: 'ctrl',
	        role: 'user'
	    }).state('admin', {
	        url: '/admin/',
	        templateUrl: TEMPLATE_URL + 'admin/dashboard.html',
	        controller: 'AdminDashboardController',
	        controllerAs: 'ctrl',
	        role: 'admin'
	    }).state('unauthorized', {
	        url: '/unauthorized/',
	        templateUrl: TEMPLATE_URL + 'unauthorized.html',
	        role: 'unauthorized'
	    });
	}).run(function ($rootScope, $q, $state, $http, $location, store, AuthService) {
	    var token = store.get('token');

	    if (token) {
	        $http.defaults.headers.common.Authorization = 'Bearer ' + token;
	    }

	    $rootScope.$on('$stateChangeStart', function (event, next, current) {
	        if (!AuthService.isAuthenticated() && current.name === 'login') {
	            event.preventDefault();
	            $state.go('login');
	        }
	    });

	    $rootScope.$on('$stateChangeStart', function (event, next, current, toState) {
	        if (!AuthService.isAuthenticated() && next.name === 'unauthorized') {
	            event.preventDefault();
	            $state.go('login');
	        }
	    });

	    $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
	        if (toState.role !== undefined && toState.role != 'anon') {
	            if (store.get('account_type') !== toState.role) {
	                event.preventDefault();
	                $location.path('/unauthorized/');
	            }
	        }
	    });

	    $rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
	        if (AuthService.isAuthenticated() && toState.role === 'anon') {
	            $location.path('/unauthorized/');
	        }
	    });
	});

/***/ })
/******/ ]);