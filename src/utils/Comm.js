/*
    此文件中函数用于处理前后端通讯
    所有通讯基于GET和POST，用axios和ajax实现
*/
import axios from "axios"
// import { reject, resolve } from "core-js/fn/promise";
import CookieOperation from "./Cookie";
// import API from "@/utils/Constants" // 不知道为什么API调用不能使用，只能直接填string形式的url，猜测可能是写了method的原因

axios.defaults.withCredentials = true;
axios.interceptors.request.use(
    function(config) {
        // 在post请求前统一添加X-CSRFToken的header信息
        let cookie = document.cookie;
        if(cookie && config.method == 'post'){
            console.log("cookie: ", cookie)
            config.headers.post['X-CSRFToken'] = CookieOperation.getCookie('csrftoken');
        }
        return config;
    },
    function(error) {
        // Do something with request error
        return Promise.reject(error);
    }
);

var id
const COMM = {
    UploadDest : {
        COURSEWARE: 1,
        TEST: 2,
        TASK: 3,
    },
    login(username, password) {
        /*
            功能：登录
            此函数的2个参数分别为未加密的用户名和密码，
            通过向后端的API POST JSON格式的信息来完成通讯
            返回一个Promise，用于反馈登录是否成功
        */
       // 对密码进行SHA256加密后再进行传输
       //var shajs = require('sha.js')
       //var passwordEncrypted = shajs('sha256').update(password).digest('hex')
       // 输入框和加密的输出调试（之后要删掉！）
       console.log("username: " + username)
       console.log("password: " + password)
       //console.log("password encrypted: " + passwordEncrypted)
       return new Promise((resolve, reject) => {
            axios.post('/api/login', { 'username': username, 'password': password}) // POST请求
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err.data)
            })
       });
    },
    createAccount(username, password, personalInfo) {
        /*
            功能：注册新用户
            此函数的3个参数分别为未加密的用户名和密码，
            以及一个个人信息表格，表格项依次为姓名、部门、城市、入职日期（2022.3.22 - 此表格可能会随着工程进一步进展做出改变）
            通过向后端的API POST JSON格式的信息来完成通讯
            返回一个Promise，用于反馈注册是否成功
        */
        //对密码进行SHA256加密
        //var shajs = require('sha.js')
        //var passwordEncrypted = shajs('sha256').update(password).digest('hex')
        //输入框、个人信息表单和加密的输出调试（之后要删掉）
        console.log("username: " + username)
        console.log("password: " + password)
        //console.log("password encrypted: " + passwordEncrypted)
        console.log("personal_info:", personalInfo)
        return new Promise((resolve, reject) => {
            axios.post('/api/join', {'username': username, 'password': password, 'personal_info': personalInfo})
            .then((response) => {
                resolve(response)
            }).catch((error) => {
                reject(error)
            })
        });
    },
    switchRole(switchTo) {
        console.log("switch to: " + switchTo)
        return new Promise((resolve, reject) => {
            axios.post('/api/switch_role', {
                "action": "switch role",
                "switch_to": switchTo,
            }).then((response) => {
                resolve(response)
            }).catch((error) => {
                reject(error)
            })
        })
    },
    getToken() {
        console.log("get token")
        return new Promise((resolve, reject) => {
            axios.get('/api/get_token')
            .then((response) => {
                resolve(response.data)
            }).catch((error) => {
                reject(error.data)
            })
        })
    },
    getCurRole() {
        console.log('get cur role')
        return new Promise((resolve, reject) => {
            axios.get('/api/get_cur_role')
            .then((response) => {
                resolve(response.data)
            }).catch((error) => {
                reject(error.data)
            })
        })
    },
    get_admin_newcomer_list(){  // 从后端获取新人列表的table信息
        return new Promise((resolve, reject) => {
            axios.get('/api/admin_newcomer_list')  // GET请求
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err)
            })
       });
    },
    get_admin_all_user_list() {
        return new Promise((resolve, reject) => {
            axios.get('/api/admin_all_user_list')  // GET请求
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err)
            })
       });  
    },
    get_duty_teacher_list(){
        return new Promise((resolve, reject) => {
            axios.get('/api/duty_teacher_list')  // GET请求
                .then(res => {
                    resolve(res.data);
                })
                .catch(err => {
                    reject(err)
                })
        });
    },
    logout(){
        return new Promise((resolve, reject) => {
            axios.get('/api/logout') // GET请求
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err.data)
            })
       });
    },
    get_newcomer_info(username){
        /*
        接受前端向api/newcomer_info的post请求
        权限：admin, teacher
        */
        return new Promise((resolve, reject) => {
            console.log('username:', username)
            axios.post('/api/newcomer_info', {'action': 'newcomer info', 'newcomer': username}) // POST请求
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err)
            })
       });
    },
    get_user_info(){
        return new Promise((resolve,reject)=>{
            console.log("getting user info");
            axios.get("/api/get_user_info")
                .then(res=>{resolve(res.data)})
                .catch(err=>{
                    reject(err)
                })
        })
    },
    get_avatar(){
        return new Promise((resolve,reject)=>{
            console.log("getting user avatar");
            axios.get("/api/avatar")
                .then(res=>{resolve(res.data)})
                .catch(err=>{reject(err)})
        })
    },
    admin_create_content_template(data){
        return new Promise((resolve,reject)=>{
            axios.POST("/api/admin_create_content_template", data)
                .then(res=>{resolve(res.data)})
                .catch(err=>{
                    reject(err)
                })
        })
    },
    get_nominate_process(){  // 获取导师旅程相关信息（手动划掉 不是这个信息）好像是满足提名条件的list
        return new Promise((resolve, reject) => {
            axios.get('/api/nominate_process') // GET请求
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err.data)
            })
       });
    },
    get_teacher_wait_list(){  // 获取导师旅程相关信息（手动划掉 不是这个信息）好像是满足提名条件的list
        return new Promise((resolve, reject) => {
            axios.get('/api/teacher_wait_list') // GET请求
                .then(res => {
                    resolve(res.data);
                })
                .catch(err => {
                    reject(err.data)
                })
        });
    },
    get_nominated_list(){  // 获取导师旅程相关信息（手动划掉 不是这个信息）好像是满足提名条件的list
        return new Promise((resolve, reject) => {
            axios.get('/api/nominated_list') // GET请求
                .then(res => {
                    resolve(res.data);
                })
                .catch(err => {
                    reject(err.data)
                })
        });
    },
    reject_nominate(username){
        return new Promise((resolve, reject) => {
            axios.post('/api/reject_nominate',{"username":username})
                .then(res => {
                    resolve(res.data);
                })
                .catch(err => {
                    reject(err.data)
                })
        });
    },
    accept_nominate(username){
        return new Promise((resolve, reject) => {
            axios.post('/api/accept_nominate',{"username":username})
                .then(res => {
                    resolve(res.data);
                })
                .catch(err => {
                    reject(err.data)
                })
        });
    },
    nominate_teachers(lists){
        return new Promise((resolve, reject) => {
            axios.post('/api/nominate_teachers',lists)
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    assign_teacher(newcomer,teacher){
        return new Promise((resolve, reject) => {
            axios.post('/api/assign_teacher',{"teacher":teacher,"newcomer":newcomer})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    get_honor(teacher){
        return new Promise((resolve, reject) => {
            axios.post('/api/get_honor',{"teacher":teacher})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    teacher_summary_info(teacher){ // 导师看板中查看自己带了多少人，何时上岗等
        return new Promise((resolve, reject) => {
            axios.post('/api/teacher_summary_info',{"teacher":teacher})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    newcomer_summary_info(){
        return new Promise((resolve, reject) => {
            axios.get('/api/newcomer_summary_info',)
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    newcomer_summary_info_by_name(newcomer){
        return new Promise((resolve, reject) => {
            axios.post('/api/newcomer_summary_info_by_name', {"newcomer": newcomer})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    teacher_board_summary_info(){
        return new Promise((resolve, reject) => {
            axios.get('/api/teacher_board_summary_info',)
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    teacher_board_summary_by_name(teacher){
        return new Promise((resolve, reject) => {
            axios.post('/api/teacher_board_summary_by_name',{"teacher":teacher})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    newcomer_score_teacher(score){
        return new Promise((resolve, reject) => {
            axios.post('/api/newcomer_score_teacher',{"score":score})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    newcomer_commit_teacher(content){
        return new Promise((resolve, reject) => {
            axios.post('/api/newcomer_commit_teacher',{"content": content})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    teacher_commit_newcomer(content, newcomer){
        return new Promise((resolve, reject) => {
            axios.post('/api/teacher_commit_newcomer',{"content": content, "newcomer":newcomer})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    teacher_score_newcomer(score, newcomer){
        return new Promise((resolve, reject) => {
            axios.post('/api/teacher_score_newcomer',{"score": score, "newcomer":newcomer})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    newcomer_recode(content, newcomer){
        return new Promise((resolve, reject) => {
            axios.post('/api/newcomer_recode',{"content": content, "newcomer":newcomer})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    get_newcomer_recode(newcomer){
        return new Promise((resolve, reject) => {
            axios.post('/api/get_newcomer_recode',{ "newcomer":newcomer})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    get_commits_and_score(newcomer){
        return new Promise((resolve, reject) => {
            axios.post('/api/get_commits_and_score',{"newcomer":newcomer})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    get_my_commit(newcomer){
        return new Promise((resolve, reject) => {
            axios.post('/api/get_my_commit',{"newcomer":newcomer})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    teacher_newcomer_list(){
        return new Promise((resolve, reject) => {
            axios.get('/api/teacher_newcomer_list',{})
                .then(res => {resolve(res.data);})
                .catch(err => {reject(err.data)})
        });
    },

    bootcamp_attend(dateRangeStart, dateRangeEnd) {  // 维度分析
        return new Promise((resolve, reject) => {
            axios.post('/api/bootcamp_attend', {"dateRangeStart": dateRangeStart, "dateRangeEnd": dateRangeEnd})
                .then(response => {
                    resolve(response.data)
                })
                .catch(error => {
                    reject(error.data)
                })
        })
    },
    newcomer_average_score(dateRangeStart, dateRangeEnd) {  // 维度分析
        return new Promise((resolve, reject) => {
            axios.post('/api/newcomer_average_score', {"dateRangeStart": dateRangeStart, "dateRangeEnd": dateRangeEnd})
                .then(response => {
                    resolve(response.data)
                })
                .catch(error => {
                    reject(error.data)
                })
        })
    },
    teacher_average_score(dateRangeStart, dateRangeEnd) {  // 维度分析
        return new Promise((resolve, reject) => {
            axios.post('/api/teacher_average_score', {"dateRangeStart": dateRangeStart, "dateRangeEnd": dateRangeEnd})
                .then(response => {
                    resolve(response.data)
                })
                .catch(error => {
                    reject(error.data)
                })
        })
    },
    camp_completion(dateRangeStart, dateRangeEnd) {  // 维度分析
        return new Promise((resolve, reject) => {
            axios.post('/api/camp_completion', {"dateRangeStart": dateRangeStart, "dateRangeEnd": dateRangeEnd})
                .then(response => {
                    resolve(response.data)
                })
                .catch(error => {
                    reject(error.data)
                })
        })
    },
    graduate_time(dateRangeStart, dateRangeEnd) {  // 维度分析
        return new Promise((resolve, reject) => {
            axios.post('/api/graduate_time', {"dateRangeStart": dateRangeStart, "dateRangeEnd": dateRangeEnd})
                .then(response => {
                    resolve(response.data)
                })
                .catch(error => {
                    reject(error.data)
                })
        })
    },
    tutor_assignment_chart(dateRangeStart, dateRangeEnd) {  // 维度分析
        return new Promise((resolve, reject) => {
            axios.post('/api/tutor_assignment_chart', {"dateRangeStart": dateRangeStart, "dateRangeEnd": dateRangeEnd})
                .then(response => {
                    resolve(response.data)
                })
                .catch(error => {
                    reject(error.data)
                })
        })
    },
    async create_default_program() {
        let cover = "NOT_A_REAL_BMP"
        var res = await axios.post('/api/create_program', {
                action: "CreateProgram",
                name: "DEFAULT",
                intro: "default program",
                tag: "default",
                recommend_time: "1",
                audience: "newcomer",
                cover: cover
        })
        id = res.data.programID
        //console.log("id:", id)
    },
    async upload_test(programID, addTestInfo) {
        // let cover = "NOT_A_REAL_BMP"
        // var res = await axios.post('/api/create_program', {
        //     action: "CreateProgram",
        //     name: "DEFAULT",
        //     intro: "default program",
        //     tag: "default",
        //     recommendTime: "1",
        //     audience: "newcomer",
        //     isTemplate: true,
        //     cover: cover
        // })
        // id = res.data.programID
        console.log("id:", id)
        return new Promise((resolve, reject) => {
            var postForm = addTestInfo
            postForm.append('type', 'exam')
            postForm.append('programID', programID)
            // the following code fills unused parts of the form
            postForm.append('taskType', 0)
            postForm.append('taskText', "")
            postForm.append('taskLink', "")
            postForm.append('taskFile', "")
            axios.post('/api/admin_create_content_template', postForm)
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err.data)
            })
        });
    },
    async upload_course(programID, classData, lessonDataList) {
        console.log(classData)
        console.log(lessonDataList)
        let cover = 'NOT_A_REAL_BMP'
        // var programRes = await axios.post('/api/create_program', {
        //     action: "CreateProgram",
        //     name: "DEFAULT",
        //     intro: "default program",
        //     tag: "default",
        //     recommendTime: "1",
        //     isTemplate: true,
        //     audience: classData.audience,
        //     cover: cover
        // })
        // var programID = programRes.data.programID
        console.log("programID:", programID)
        console.log('classData', classData);
        var classDataForm = new FormData()
        classDataForm.append('action', 'CreateContentTemplate')
        classDataForm.append('name', classData.name)
        classDataForm.append('intro', classData.intro)
        classDataForm.append('tag', classData.tag)
        classDataForm.append('recommendTime', classData.recommendTime)
        classDataForm.append('audience', classData.audience)
        classDataForm.append('cover', cover)
        classDataForm.append('type', 'course')
        classDataForm.append('isTemplate', classData.isTemplate)
        classDataForm.append('csv', '')
        classDataForm.append('programID', programID)
        classDataForm.append('taskType', 0)
        classDataForm.append('taskText', '')
        classDataForm.append('taskLink', '')
        classDataForm.append('taskFile', '')
        classDataForm.append('isObligatory', classData.isObligatory)
        console.log('classDataForm', classDataForm.tag);
        var contentRes = await axios.post('./api/admin_create_content_template', classDataForm)
        var contentID = contentRes.data.contentID
        console.log("contentID:", contentID)
        console.log(lessonDataList)
        lessonDataList.forEach(async lessonData => {
            var lessonDataForm = new FormData()
            console.log(lessonData)
            lessonDataForm.append('action', 'CreateLessonTemplate')
            lessonDataForm.append('name', lessonData.name)
            lessonDataForm.append('intro', lessonData.intro)
            lessonDataForm.append('recommendTime', lessonData.recommendTime)
            lessonDataForm.append('cover', cover)
            lessonDataForm.append('contentID', contentID)
            lessonDataForm.append('programID', programID)
            lessonData.coursewares.forEach((coursewareFile, index, array) => {
                lessonDataForm.append('file' + String(index), coursewareFile)
                console.log(array[index])
            });
            var lessonRes = await axios.post('./api/create_lesson', lessonDataForm)
            console.log(lessonRes.data)
        });
    },
    async upload_task(programID, task_data) {
        console.log('upload task')
        console.log(task_data.get('audience'))
        // let cover = 'NOT_A_REAL_BMP'
        // var programRes = await axios.post('/api/create_program', {
        //     action: "CreateProgram",
        //     name: "DEFAULT",
        //     intro: "default program",
        //     tag: "default",
        //     recommendTime: "1",
        //     isTemplate: true,
        //     audience: task_data.get('audience'),
        //     cover: cover
        // })
        // var programID = programRes.data.programID
        task_data.append('programID', programID)
        console.log('task_data', task_data)
        return new Promise((resolve, reject) => {
            axios.post('/api/admin_create_content_template', task_data)
            .then(res => {
                resolve(res.data);
            })
            .catch(err => {
                reject(err.data)
            })
        })
    },
    // upload_info(id, order, /*cover,*/ type){
    //     let cover = "NOT_A_REAL_BMP"
    //     switch(type){
    //         case COMM.UploadDest.COURSEWARE:
    //             return new Promise((resolve, reject) => {
    //                 axios.post('/api/upload_courseware_info', {
    //                     order: order,
    //                     lessonID: id,
    //                     cover: cover
    //                 })
    //                 .then(res => {
    //                     resolve(res.data);
    //                 })
    //                 .catch(err => {
    //                     reject(err.data)
    //                 })
    //             });
    //         case COMM.UploadDest.TEST:
    //             //TODO
    //             break
    //         case COMM.UploadDest.TASK:
    //             //TODO
    //             break
    //         default:
    //             break
    //     }
    // },
    // upload_file(item, type){
    //     let formData = new FormData()
    //     let file = item.raw
    //     formData.append('content', file) 
    //     switch(type) {
    //         case COMM.UploadDest.COURSEWARE:
    //             //TODO
    //             return new Promise((resolve, reject) => {
    //                 axios.post('/api/upload_courseware_file', formData)
    //                 .then(res => {
    //                     resolve(res.data);
    //                 })
    //                 .catch(err => {
    //                     reject(err.data)
    //                 })
    //             });
    //         case COMM.UploadDest.TEST:
    //             //TODO
    //             break
    //         case COMM.UploadDest.TASK:
    //             //TODO
    //             break
    //         default:
    //             break
    //     }
    // },
    // upload_test_file(form){
    //     /* 上传testfile（csv文件） */
    //     return new Promise((resolve, reject) => {
    //         axios({
    //             url: 'api/upload_test_file',
    //             data: form,
    //             method: 'POST',
    //             contentType: 'multipart/form-data',
    //             processData: false,  // 告诉jquery不要对form进行处理
    //             // contentType: false,  // 指定为false才能形成正确的Content-Type
    //         })
    //         .then(function(res) {
    //             resolve(res.data)
    //         })
    //         .catch(function(err) {
    //             reject(err.data)
    //         })
    //    });
    // },
    upload_lesson_file(form){
        /* 上传课件（pptx文件） */
        return new Promise((resolve, reject) => {
            axios({
                url: 'api/upload_lesson_file',
                data: form,
                method: 'POST',
                contentType: 'multipart/form-data',
                processData: false,  // 告诉jquery不要对form进行处理
                // contentType: false,  // 指定为false才能形成正确的Content-Type
            })
            .then(function(res) {
                resolve(res.data)
            })
            .catch(function(err) {
                reject(err.data)
            })
       });
    },
    downloadTestInfoByID(testID) {
        return new Promise((resolve, reject) => {
            axios({
                url: 'api/download_test_info',
                data: {action: "retrieve test info", testID: testID},
                method: 'POST',
                contentType: 'application/json',
            })
            .then(res => {
                resolve(res.data)
            })
            .catch(err => {
                reject(err.data)
            })
        });
    },
    downloadTestPaperByID(testID) {
        return new Promise((resolve, reject) => {
            axios({
                url: 'api/download_test_paper',
                data: {action: "retrieve test paper", testID: testID},
                method: 'POST',
                contentType: 'application/json',
            })
            .then(res => {
                resolve(res.data)
            })
            .catch(err => {
                reject(err.data)
            })
        });
    },
    get_teacher_newcomer_list() {  // 获取导师的带新看板中的新人列表
        return new Promise((resolve, reject) => {
            axios.get('/api/teacher_newcomer_list')
            .then(response => {resolve(response.data)})
            .catch(error => {reject(error.data)})
        })
    },

    get_teacher_newcomer_list_by_name(teacher) {  // 获取导师的带新看板中的新人列表
        return new Promise((resolve, reject) => {
            axios.post('/api/teacher_newcomer_list_by_name',{"teacher":teacher})
                .then(response => {resolve(response.data)})
                .catch(error => {reject(error.data)})
        })
    },

    upload_test_answers(testID, answer) {  // 用户交卷时上传自己的答案，在后端判卷
        return new Promise((resolve, reject) => {
            axios.post(
                '/api/upload_answers',
                {
                    'action': 'grade test',
                    'testID': testID,
                    'answer': answer,
                }
            )
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    my_course_list() {  // 获取学习课程的课程清单
        return new Promise((resolve, reject) => {
            axios.get('/api/my_course_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    assignable_course_list() {  // 获取分配课程的课程清单
        return new Promise((resolve, reject) => {
            axios.get('/api/assignable_course_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    my_test_list() {  // 获取做考试的考试清单
        return new Promise((resolve, reject) => {
            axios.get('/api/my_test_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    assignable_test_list() {  // 获取分配考试的考试清单
        return new Promise((resolve, reject) => {
            axios.get('/api/assignable_test_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    my_task_list() {  // 获取做任务的考试清单
        return new Promise((resolve, reject) => {
            axios.get('/api/my_task_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    assignable_task_list() {  // 获取分配任务的考试清单
        return new Promise((resolve, reject) => {
            axios.get('/api/assignable_task_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    retrieveTaskFileByID(taskID) {
        return new Promise((resolve, reject) => {
            axios({
                method: 'post',
                url: '/api/task_file_by_id',
                data: {'action': 'task file by id', 'taskID': taskID},
                responseType: 'blob'
            })
            .then(response => {
                resolve(response)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    program_template_list() {
        return new Promise((resolve, reject) => {
            axios.get('/api/program_templates')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    create_template_program(name, intro, tag, recommendTime, audience, cover, isTemplate) {
        return new Promise((resolve, reject) => {
            axios.post('/api/create_program', {
                "action": "CreateProgram",
                "name": name,
                "intro": intro,
                "tag": tag,
                "recommendTime": recommendTime,
                "audience": audience,
                "cover": cover,
                "isTemplate": isTemplate,
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    program_content_list(programID) {
        return new Promise((resolve, reject) => {
            axios.post('/api/program_content_list', {
                'action': 'get content list for program', 
                'programID': programID
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    finishTask(taskID) {
        return new Promise((resolve, reject) => {
            axios.post('/api/finish_task', {
                'action': 'finish task',
                'taskID': taskID
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },

    finish_all_lesson(username){
        return new Promise((resolve, reject) => {
            axios.post('/api/finish_all_lesson', {"username":username,})
                .then(response => {resolve(response.data)})
                .catch(error => {reject(error.data)})
        })
    },


    assignable_program_list() {
        return new Promise((resolve, reject) => {
            axios.get('/api/assignable_program_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    copy_program_template(programID) {
        return new Promise((resolve, reject) => {
            axios.post('/api/copy_program_template', {
                'action': 'copy program template', 
                'programID': programID
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    assign_program(username, programID) {
        return new Promise((resolve, reject) => {
            axios.post('/api/assign_program', {
                'action': 'assign program',
                'username': username,
                'programID': programID
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    has_program(username, audience) {
        return new Promise((resolve, reject) => {
            axios.post('/api/has_program', {
                'action': 'has program',
                'username': username,
                'audience': audience,
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    assign_content_to_program(programID, contentID) {
        return new Promise((resolve, reject) => {
            axios.post('/api/assign_content_to_program', {
                'action': 'assign content to program',
                'programID': programID,
                'contentID': contentID,
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    async content_progress(programID, contentID) {
        return new Promise((resolve, reject) => {
            axios.post('/api/content_progress', {
                'action': 'check content progress',
                'programID': programID,
                'contentID': contentID,
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    begin_test(testID){
        return new Promise((resolve, reject) => {
            axios.post('/api/begin_test', {
                'action': 'start test',
                'testID': testID,
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    content_lesson_list(courseID){
        return new Promise((resolve, reject) => {
            axios.post('/api/content_lesson_list', {
                'action': 'lesson list for course',
                'contentID': courseID,
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    create_notification(apiData) {
        return new Promise((resolve, reject) => {
            axios.post('api/create_notification', apiData)
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    lesson_courseware_list(lessonID){
        return new Promise((resolve, reject) => {
            axios.post('/api/lesson_courseware_list', {
                'action': 'courseware list for lesson',
                'lessonID': lessonID,
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    retrieve_notifications() {
        return new Promise((resolve, reject) => {
            axios.get('api/my_notification_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    finish_lesson(username, lessonID){
        return new Promise((resolve, reject) => {
            axios.post('/api/finish_lesson', {
                'username': username,
                'lessonID': lessonID,
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    finish_notification(notificationID) {
        return new Promise((resolve, reject) => {
            axios.post('api/finish_notification', {
                'action': 'finish notification',
                'notificationID': notificationID
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    retrieve_group() {
        return new Promise((resolve, reject) => {
            axios.get('api/my_group_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    create_group(postData) {
        return new Promise((resolve, reject) => {
            axios.post('api/create_group', postData)
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    add_group_member(postData) {
        return new Promise((resolve, reject) => {
            axios.post('api/add_group_member', postData)
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    create_group_notification(postData) {
        return new Promise((resolve, reject) => {
            axios.post('api/create_group_notification', postData)
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    retrieve_authored_notification() {
        return new Promise((resolve, reject) => {
            axios.get('api/authored_notification_list')
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    delete_notification(postData) {
        return new Promise((resolve, reject) => {
            axios.post('api/delete_notification', postData)
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    delete_member(postData) {
        return new Promise((resolve, reject) => {
            axios.post('api/delete_member', postData)
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    delete_group(postData) {
        return new Promise((resolve, reject) => {
            axios.post('api/delete_group', postData)
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
    delete_content_from_program(programID, contentID) {
        return new Promise((resolve, reject) => {
            axios.post('api/delete_content_from_program', {
                "action": "delete content from program",
                "programID": programID,
                "contentID": contentID,
            })
            .then(response => {
                resolve(response.data)
            })
            .catch(error => {
                reject(error.data)
            })
        })
    },
}

export default COMM