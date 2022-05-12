<template>
<v-container>
    <!-- 考试信息 -->
    <v-card v-if="testStatus === 'unstarted'" elevation="0">
        <v-card-text v-if='false' style="margin-top: 10px">
            <h3 class="text-center">{{ testInfo.intro }}</h3>
        </v-card-text>
        <v-card-text>
            <div class="text-center">
                <v-btn large @click="getTestQuestion">开始考试</v-btn>
            </div>
        </v-card-text>
    </v-card>
    <div v-else-if="testStatus === 'started'">
        <!-- 计时器 -->
        <v-card-title>
            计时：{{timer.hour}}<span>:</span>{{timer.min}}<span>:</span>{{timer.sec}}
        </v-card-title>
        <!-- 题目与选项 -->
        <v-card-text>
        <template v-for="(test_question, i) in testQuestions">
            <!-- <v-radio-group v-model="test_question.radios" :key="i" multiple>
                <template v-slot:label>
                    <h2>{{i + 1}}. {{ test_question.question }}</h2>
                </template>
                <v-radio v-for="(choice, j) in test_question.choices" :key="j" :value="j">
                    <template v-slot:label>
                        <div>{{ testIndex[j] }}. {{ choice }}</div>
                    </template>
                </v-radio>
            </v-radio-group> -->
            <div :key="i">
                <h2 style="margin-top: 20px; margin-bottom: 20px">{{i + 1}}. {{ test_question.question }}</h2>
                <v-checkbox
                    style="margin-left: 20px; margin-top: -5px; margin-bottom: -15px"
                    v-model="test_question.radios"
                    v-for="(choice, j) in test_question.choices" 
                    :key="j" 
                    :value="j"
                    :label="`${testIndex[j]}. ${choice}`"
                >
                </v-checkbox>
            </div>

        </template>
        </v-card-text>
        <!-- 提交试卷 -->
        <v-card-actions>
        <v-btn @click="submit">交卷</v-btn>
        </v-card-actions>
    </div>
    <!-- 考试结果 -->
    <v-card v-else-if="testStatus === 'finished'" elevation="0">
        <v-card-title>答题情况</v-card-title>
        <v-card-text><h3>分数 {{ score }}/100</h3></v-card-text>
        <!-- 计时器 -->
        <v-card-title>
            您用时：{{timer.hour}}<span>:</span>{{timer.min}}<span>:</span>{{timer.sec}}
        </v-card-title>
        <!-- 题目与选项 -->
        <v-card-text>
            <template v-for="(test_answer, i) in testAnswers">
                <!-- <v-radio-group v-model="test_answer.radios" :key="i" multiple>
                    <template v-slot:label>
                        <h2>{{i + 1}}. {{ test_answer.question }}</h2>
                    </template> -->
                    <!-- TODO: 有自己选择的错误答案+正确答案 -->
                    <!-- <v-radio v-for="(choice, j) in test_answer.choices" :key="j" :value="j" :color="choice.color">
                        <template v-slot:label>
                            <div>{{ testIndex[j] }}. {{ choice.text }}</div>
                        </template>
                    </v-radio>
                    <p>正确答案是<span v-for="(result, k) in results[i][1]" :key="k">{{ testIndex[result] }}</span>，您选择了<span v-for="(result, k) in results[i][0]" :key="k">{{ testIndex[result] }}</span></p>
                </v-radio-group> -->
                <div :key="i">
                    <h2 style="margin-top: 20px; margin-bottom: 20px">{{i + 1}}. {{ test_answer.question }}</h2>
                    <v-checkbox
                        style="margin-left: 20px; margin-top: -5px; margin-bottom: -15px"
                        v-model="test_answer.radios"
                        v-for="(choice, j) in test_answer.choices" 
                        :key="j" 
                        :value="j"
                        :color="choice.color"
                        :label="`${testIndex[j]}. ${choice.text}`"
                    >
                    </v-checkbox>
                    <p>正确答案是<span v-for="(result, k) in results[i][1]" :key="k">{{ testIndex[result] }}</span><span v-if="results[i][0].length === 0">，您未选择任何选项</span><span v-else>，您选择了<span v-for="(result, k) in results[i][0]" :key="k">{{ testIndex[result] }}</span></span></p>
                </div>

            </template>
        </v-card-text>
    </v-card>
</v-container>
</template>

<script>
// 考试试卷的组件封装
import COMM from '@/utils/Comm.js'

export default ({
    name: 'TestList',
    inject: ['GLOBAL'],
    data() {
        return {      
            // 计时器
            flag: null, 
            timer: {
                hour: '00',
                min: '00',
                sec: '00', 
                hour_tick: 0,
                min_tick: 0, 
                sec_tick: 0,
            },
            testStatus: 'unstarted', // 是否开始考试
            testIndex: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
            testInfo: {
                title: '游泳测试',
                id: '123',
                intro: '这是一段平平无奇的考试的介绍'
            },
            testQuestions: [
                // {
                //     question: '1 + 1 =',
                //     choices: [
                //         '0', '1', '2', '3',
                //     ],
                //     radios: '',
                // },
                // {
                //     question: '2 + 4 =',
                //     choices: [
                //         '0', '1', '3', '6',
                //     ],
                //     radios: '',
                // },
                // {
                //     question: '3 + 7 =',
                //     choices: [
                //         '3', '5', '8', '10',
                //     ],
                //     radios: '',
                // },
            ],
            testAnswers: [
                // {
                //     question: '1 + 1 =',
                //     choices: [
                //         {text: '0', color: 'error'}, 
                //         {text: '1', color: 'error'}, 
                //         {text: '2', color: 'success'}, 
                //         {text: '3', color: 'error'},
                //     ],
                //     radios: '',
                // },
                // {
                //     question: '2 + 4 =',
                //     choices: [
                //         {text: '0', color: 'error'}, 
                //         {text: '1', color: 'error'}, 
                //         {text: '3', color: 'error'}, 
                //         {text: '6', color: 'success'},
                //     ],
                //     radios: '',
                // },
                // {
                //     question: '3 + 7 =',
                //     choices: [
                //         {text: '3', color: 'error'}, 
                //         {text: '5', color: 'error'}, 
                //         {text: '8', color: 'error'}, 
                //         {text: '10', color: 'success'},
                //     ],
                //     radios: '',
                // },
            ],
            score: '',
            results: [],
        }
    },
    props: {
        testItem: {},  // 弃用这个
        // 调用TestList的时候传进来contentID，然后TestList自己向后端请求这个Test的相关信息
        // 然后做题的时候需要知道是哪个用户，用this.GLOBAL.username获取
        contentID: {
            type: String,
        },
    },
    methods: {
        getTestInfo() {
            // TODO: 从后端获取考试信息
            // console.log('testItem:', this.testItem);
            // this.testInfo = this.testItem.test_info;
            // this.testQuestions = this.testItem.test_paper;
            // this.testAnswers = this.testItem.test_paper;
        },
        startTimer(){
            this.flag = setInterval(()=>{
            if(this.timer.sec === 60 || this.timer.sec === '60'){
                this.timer.sec = '00';
                this.timer.sec_tick = 0;
                if(this.timer.min === 60 || this.timer.min === '60'){
                this.timer.min = '00';
                this.timer.min_tick = 0;
                if(this.timer.hour_tick+1 <= 9){
                this.timer.hour_tick++;
                this.timer.hour = '0' + this.timer.hour_tick;
                }else{
                this.timer.hour_tick++;
                this.timer.hour = this.timer.hour_tick;
                }
                }else{
                if(this.timer.min_tick+1 <= 9){
                this.timer.min_tick++;
                this.timer.min = '0' + this.timer.min_tick;
                }else{
                this.timer.min_tick++;
                this.timer.min = this.timer.min_tick;
                }
                }
            }else{
                if(this.timer.sec_tick+1 <= 9){
                this.timer.sec_tick++;
                this.timer.sec = '0' + this.timer.sec_tick;
                }else{
                this.timer.sec_tick++;
                this.timer.sec=this.timer.sec_tick;
                }
            }
            }, 1000)
        },
        endTimer(){
            this.flag = clearInterval(this.flag)
        },
        getTestQuestion() {
            this.testStatus = 'started';
            // TODO: 从后端获取题目列表
            COMM.begin_test(this.contentID).then(res => {
                console.log("get begin_test: ", res)
                this.testQuestions = res.test;
                this.testAnswers = res.test;
                
                // 开始计时
                this.startTimer();

            }, err => {
                console.log("get begin_test error: ", err)
            })
        },
        parseTestResults(testResults){
            for(var i = 0; i < testResults.length; i++){
                var choices = this.testAnswers[i].choices; // 列表，形如['0', '1', '2', '3',],
                this.testAnswers[i].choices = [];
                for(var l = 0; l < choices.length; l++){
                    this.testAnswers[i].choices.push({text: choices[l], color: 'error'})
                }

                var testResult = testResults[i];
                for(var j = 0; j < testResult[0].length; j++){
                    testResult[0][j] = testResult[0][j].charCodeAt(0) - 65;
                }

                // 正确答案
                for(var k = 0; k < testResult[1].length; k++){
                    testResult[1][k] = testResult[1][k].charCodeAt(0) - 65;
                    this.testAnswers[i].choices[testResult[1][k]] = {text: choices[testResult[1][k]], color: 'success'};
                }     
            }
            console.log('testResults new', testResults)
        },
        submit() {
            this.testStatus = 'finished';  // 用于渲染页面
            // 发送答案至后端进行判卷
            var test_questions = this.testQuestions;
            var answer = [];
            for(var i = 0; i < test_questions.length; i++){
                answer.push(test_questions[i].radios);
                this.testAnswers[i].radios = test_questions[i].radios;
            }
            console.log('answer by user: ', answer); // 用户做的答案

            COMM.upload_test_answers(this.contentID, answer).then(res => {
                console.log("upload_test_answers: ", res)
                this.score = res.results[0];
                this.results = res.results[1];
                this.parseTestResults(res.results[1]);

                // 停止计时
                this.endTimer();
                
            }, err => {
                console.log("upload_test_answers error: ", err)
            })
        },
    },
    mounted() {
        console.log('contentID', this.contentID);
        this.getTestInfo();
    }
})
</script>
