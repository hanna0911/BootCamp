<template>
<v-container>
    <h2 class="px-4 pt-4 pb-3 font-weight-black">维度分析</h2>

    <!-- 新人数据日期栏 -->
    <div style="margin: 1%" class="block">
        <el-date-picker
            v-model="newcomerDateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :default-time="['00:00:00', '23:59:59']">
        </el-date-picker>
    </div>

    <!-- 第一行新人数据 -->
    <v-row no-gutters>
        
        <!-- Bootcamp 参与率 -->
        <v-col>
            <v-card outlined style="margin: 2%">
                <v-card-title>Bootcamp 参与率</v-card-title>
                <v-divider/>
                <v-card-text>
                <div id="bootcampChart" :style="{ height: '300px'}"></div>
                </v-card-text> 
            </v-card>
        </v-col>

        <!-- 新人平均分 -->
        <v-col>
            <v-card outlined style="margin: 2%">
                <v-card-title>新人平均分</v-card-title>
                <v-divider/>
                <v-card-text>
                    <div :style="{ height: '300px'}">
                        <v-card color="#dcdcdc" style="height: 46%; margin-bottom: 4%">
                            <v-card-text>
                                <v-row style="margin: 30px">
                                    <v-col>
                                        团队新人
                                    </v-col>
                                    <v-col>
                                        <h1>{{ newcomerScore.group }} / 10.0</h1>
                                    </v-col>
                                </v-row>
                                </v-card-text>
                        </v-card>
                        <v-card color="#dcdcdc" style="height: 46%; margin-top: 4%">
                            <v-card-text>
                                <v-row style="margin: 30px">
                                    <v-col>
                                        全平台Bootcamp新人
                                    </v-col>
                                    <v-col>
                                        <h1>{{ newcomerScore.all }} / 10.0</h1>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </div>
                </v-card-text> 
            </v-card>
        </v-col>
    </v-row>

    <!-- 第二行新人数据 -->
    <v-row no-gutters>

        <!-- 培训完成情况 -->
        <v-col>
            <v-card outlined style="margin: 2%">
                <v-card-title>培训完成情况</v-card-title>
                <v-divider/>
                <v-card-text>
                <div id="completionChart" :style="{ height: '300px'}"></div>
                </v-card-text> 
            </v-card>
        </v-col>

        <!-- 毕业时间跨度 -->
        <v-col>
            <v-card outlined style="margin: 2%">
                <v-card-title>毕业时间跨度</v-card-title>
                <v-divider/>
                <v-card-text>
                <div id="graduatetimeChart" :style="{ height: '300px'}"></div>
                </v-card-text> 
            </v-card>
        </v-col>
    </v-row>


    <!-- 导师数据日期栏 -->
    <div style="margin: 1%" class="block">
        <el-date-picker
            v-model="teacherDateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :default-time="['00:00:00', '23:59:59']">
        </el-date-picker>
    </div>

    <!-- 导师数据 -->
    <v-row no-gutters>

        <!-- 导师分配率 -->
        <v-col>
            <v-card outlined style="margin: 2%">
                <v-card-title>导师分配率</v-card-title>
                <v-divider/>
                <v-card-text>
                    <div id="tutorassignChart" :style="{ height: '300px'}"></div>
                </v-card-text> 
            </v-card>
        </v-col>

        <!-- 导师平均分 -->
        <v-col>
            <v-card outlined style="margin: 2%">
                <v-card-title>导师平均分</v-card-title>
                <v-divider/>
                <v-card-text>
                    <div :style="{ height: '300px'}">
                        <v-card color="#dcdcdc" style="height: 46%; margin-bottom: 4%">
                            <v-card-text>
                                <v-row style="margin: 30px">
                                    <v-col>
                                        团队导师
                                    </v-col>
                                    <v-col>
                                        <h1>{{ tutorScore.group }} / 10.0</h1>
                                    </v-col>
                                </v-row>
                                </v-card-text>
                        </v-card>
                        <v-card color="#dcdcdc" style="height: 46%; margin-top: 4%">
                            <v-card-text>
                                <v-row style="margin: 30px">
                                    <v-col>
                                        全平台Bootcamp导师
                                    </v-col>
                                    <v-col>
                                        <h1>{{ tutorScore.all }} / 10.0</h1>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>
                    </div>
                </v-card-text> 
            </v-card>
        </v-col>
    </v-row>
</v-container>
</template>

<script>

import COMM from "@/utils/Comm";

export default ({
    name: 'DimensionAnalysis',
    data() {
        return {
            pickerOptions: {
                shortcuts: [{
                    text: '最近一周',
                    onClick(picker) {
                    const end = new Date();
                    const start = new Date();
                    start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                    picker.$emit('pick', [start, end]);
                    }
                }, {
                    text: '最近一个月',
                    onClick(picker) {
                    const end = new Date();
                    const start = new Date();
                    start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                    picker.$emit('pick', [start, end]);
                    }
                }, {
                    text: '最近三个月',
                    onClick(picker) {
                    const end = new Date();
                    const start = new Date();
                    start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                    picker.$emit('pick', [start, end]);
                    }
                }],
            },
            newcomerDateRange: '',
            teacherDateRange: '',
            newcomerScore: { 
                group: '',
                all: '',
            },
            tutorScore: {
                group: '', 
                all: '', 
            }
        }
    },
    // mounted() {
    //     this.joinBootcampChart();
    //     this.averageScore();
    //     this.campCompletionChart();
    //     this.graduateTimeChart();
    //     this.tutorAssignChart();
    // },
    methods: {
        updateNewcomerAnalysis() {
            var startDate = new Date(this.newcomerDateRange[0]).getTime()
            var endDate = new Date(this.newcomerDateRange[1]).getTime()
            this.joinBootcampChart(startDate, endDate)
            this.newcomerAverageScore(startDate, endDate)
            this.campCompletionChart(startDate, endDate)
            this.graduateTimeChart(startDate, endDate)
        },
        updateTeacherAnalysis() {
            var startDate = new Date(this.teacherDateRange[0]).getTime()
            var endDate = new Date(this.teacherDateRange[1]).getTime()
            this.teacherAverageScore(startDate, endDate)
            this.tutorAssignChart(startDate, endDate)
        },
        joinBootcampChart(startDate, endDate){
            let bootcampChart = this.$echarts.init(document.getElementById('bootcampChart')) // 基于准备好的dom，初始化echarts实例
            
            // DONE: 从后端获取不同Week的入职总人数等数据
            var days = ['Week 9', 'Week 8', 'Week 7', 'Week 6', 'Week 5', 'Week 4', 'Week 3']
            var totalEmploy = [250, 240, 230, 235, 260, 280, 240];
            var school = [120, 140, 130, 150, 100, 110, 100];
            var society = [100, 80, 70, 50, 30, 40, 80];
            var intern = [20, 10, 20, 15, 100, 30, 25];
            var unselect = [10, 10, 10, 20, 30, 100, 35];
            var joinBootcamp = [170, 150, 160, 170, 180, 190, 160];

            var joinBootcampPercentage = []  // 根据joinBootcamp、totalEmploy计算出参与培训比例
            for(var i = 0; i < totalEmploy.length; i++){
                joinBootcampPercentage[i] = Math.round(joinBootcamp[i] / totalEmploy[i] * 100);
            }

            COMM.bootcamp_attend(startDate, endDate)
            .then(response => {
                console.log(response.data)
                days = response.data.days
                totalEmploy = response.data.totalEmploy
                school = response.data.school
                society = response.data.society
                intern = response.data.intern
                unselect = response.data.unselect
                joinBootcamp = response.data.joinBootcamp

                for(var i = 0; i < totalEmploy.length; i++){
                    joinBootcampPercentage[i] = Math.round(joinBootcamp[i] / totalEmploy[i] * 100);
                }
                
                bootcampChart.setOption({
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                        type: 'shadow'
                        }
                    },
                    legend: {},
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: [
                        {
                        type: 'category',
                        data: days
                        }
                    ],
                    yAxis: [
                        {
                        type: 'value',
                        name: '人数',
                        min: 0,
                        axisLabel: {
                            formatter: '{value} 人'
                        }
                        },
                        {
                        type: 'value',
                        name: '百分比',
                        min: 0,
                        axisLabel: {
                            formatter: '{value}%'
                        }
                        }
                    ],
                    series: [
                        {
                        name: '入职总人数',
                        type: 'bar',
                        yAxisIndex: 0,
                        emphasis: {
                            focus: 'series'
                        },
                        tooltip: {
                            valueFormatter: function (value) {
                            return value + ' 人';
                            }
                        },
                        data: totalEmploy 
                        },
                        {
                        name: '校招',
                        type: 'bar',
                        yAxisIndex: 0,
                        stack: 'count',
                        emphasis: {
                            focus: 'series'
                        },
                        tooltip: {
                            valueFormatter: function (value) {
                            return value + ' 人';
                            }
                        },
                        data: school
                        },
                        {
                        name: '社招',
                        type: 'bar',
                        yAxisIndex: 0,
                        stack: 'count',
                        emphasis: {
                            focus: 'series'
                        },
                        tooltip: {
                            valueFormatter: function (value) {
                            return value + ' 人';
                            }
                        },
                        data: society
                        },
                        {
                        name: '实习',
                        type: 'bar',
                        yAxisIndex: 0,
                        stack: 'count',
                        emphasis: {
                            focus: 'series'
                        },
                        tooltip: {
                            valueFormatter: function (value) {
                            return value + ' 人';
                            }
                        },
                        data: intern
                        },
                        {
                        name: '未选择',
                        type: 'bar',
                        yAxisIndex: 0,
                        stack: 'count',
                        emphasis: {
                            focus: 'series'
                        },
                        tooltip: {
                            valueFormatter: function (value) {
                            return value + ' 人';
                            }
                        },
                        data: unselect
                        },
                        {
                        name: '参与培训比例',
                        type: 'line',
                        yAxisIndex: 1,
                        emphasis: {
                            focus: 'series'
                        },
                        tooltip: {
                            valueFormatter: function (value) {
                            return value + '%';
                            }
                        },
                        data: joinBootcampPercentage
                        },
                    ]
                });
            }, error => {
                console.log(error.data)
            })
        },
        newcomerAverageScore(startDate, endDate){
            // DONE: 从后端获取新人、导师平均分（注意更改的时候要改成字符串格式）
            COMM.newcomer_average_score(startDate, endDate).then(
                response => {
                    console.log(response.data)
                    this.newcomerScore = { group: response.data.group.toFixed(2), all: response.data.all.toFixed(2) }
                },
                error => {
                    console.log(error)
                }
            )
        },
        teacherAverageScore(startDate, endDate){
            // DONE: 从后端获取新人、导师平均分（注意更改的时候要改成字符串格式）
            COMM.teacher_average_score(startDate, endDate).then(
                response => {
                    console.log(response.data)
                    this.tutorScore = { group: response.data.group.toFixed(2), all: response.data.all.toFixed(2) }
                },
                error => {
                    console.log(error)
                }
            )
        },
        campCompletionChart(startDate, endDate){
            let completionChart = this.$echarts.init(document.getElementById('completionChart')) // 基于准备好的dom，初始化echarts实例

            // DONE: 从后端获取不同Week的毕业总人数等数据
            var days = ['Week 9', 'Week 8', 'Week 7', 'Week 6', 'Week 5', 'Week 4', 'Week 3']
            var normalGraduate = [120, 140, 130, 135, 125, 115, 105];
            var totalGraduate = [210, 215, 225, 220, 225, 220, 205];

            // 根据normalGraduate、totalGraduate计算出非正常毕业人数、正常毕业比例
            var abnormalGraduate = [];
            var normalGraduatePercentage = []
            for(var i = 0; i < normalGraduate.length; i++){
                abnormalGraduate[i] = totalGraduate[i] - normalGraduate[i];
                normalGraduatePercentage[i] = Math.round(normalGraduate[i] / totalGraduate[i] * 100);
            }

            COMM.camp_completion(startDate, endDate).then(
                response => {
                    console.log(response.data)
                    days = response.data.days
                    normalGraduate = response.data.normalGraduate
                    totalGraduate = response.data.totalGraduate
                    for(var i = 0; i < normalGraduate.length; i++){
                        abnormalGraduate[i] = totalGraduate[i] - normalGraduate[i];
                        normalGraduatePercentage[i] = Math.round(normalGraduate[i] / totalGraduate[i] * 100);
                    }
                    completionChart.setOption({
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                            type: 'shadow'
                            }
                        },
                        legend: {},
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                        },
                        xAxis: [
                            {
                            type: 'category',
                            data: days
                            }
                        ],
                        yAxis: [
                            {
                            type: 'value',
                            name: '人数',
                            min: 0,
                            axisLabel: {
                                formatter: '{value} 人'
                            }
                            },
                            {
                            type: 'value',
                            name: '百分比',
                            min: 0,
                            axisLabel: {
                                formatter: '{value}%'
                            }
                            }
                        ],
                        series: [
                            {
                            name: '正常毕业人数',
                            type: 'bar',
                            yAxisIndex: 0,
                            emphasis: {
                                focus: 'series'
                            },
                            tooltip: {
                                valueFormatter: function (value) {
                                return value + ' 人';
                                }
                            },
                            data: normalGraduate 
                            },
                            {
                            name: '非正常毕业人数',
                            type: 'bar',
                            yAxisIndex: 0,
                            emphasis: {
                                focus: 'series'
                            },
                            tooltip: {
                                valueFormatter: function (value) {
                                return value + ' 人';
                                }
                            },
                            data: abnormalGraduate
                            },
                            {
                            name: '正常毕业比例',
                            type: 'line',
                            yAxisIndex: 1,
                            emphasis: {
                                focus: 'series'
                            },
                            tooltip: {
                                valueFormatter: function (value) {
                                return value + '%';
                                }
                            },
                            data: normalGraduatePercentage
                            },
                        ]
                    });
                },
                error => {
                    console.log(error)
                }
            )

        },
        graduateTimeChart(startDate, endDate){
            let graduatetimeChart = this.$echarts.init(document.getElementById('graduatetimeChart')) // 基于准备好的dom，初始化echarts实例
            
            // DONE: 从后端获取不同Week的毕业时间跨度等数据
            var days = ['Week 9', 'Week 8', 'Week 7', 'Week 6', 'Week 5', 'Week 4', 'Week 3']
            var groupAverageGraduateTime = [120, 130, 130, 115, 125, 115, 105];
            var totalAverageGraduateTime = [130, 135, 140, 120, 130, 130, 120];

            COMM.graduate_time(startDate, endDate).then(
                response => {
                    console.log(response.data)
                    days = response.data.days
                    groupAverageGraduateTime = response.data.groupAverageGraduateTime
                    totalAverageGraduateTime = response.data.totalAverageGraduateTime
                    graduatetimeChart.setOption({
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                            type: 'shadow'
                            }
                        },
                        legend: {},
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                        },
                        xAxis: [
                            {
                            type: 'category',
                            data: days
                            }
                        ],
                        yAxis: [
                            {
                            type: 'value',
                            name: '人数',
                            min: 0,
                            axisLabel: {
                                formatter: '{value}天'
                            }
                            }
                        ],
                        series: [
                            {
                            name: '部门新人',
                            type: 'bar',
                            yAxisIndex: 0,
                            emphasis: {
                                focus: 'series'
                            },
                            tooltip: {
                                valueFormatter: function (value) {
                                return value + '天';
                                }
                            },
                            data: groupAverageGraduateTime 
                            },
                            {
                            name: '全平台新人',
                            type: 'bar',
                            yAxisIndex: 0,
                            emphasis: {
                                focus: 'series'
                            },
                            tooltip: {
                                valueFormatter: function (value) {
                                return value + '天';
                                }
                            },
                            data: totalAverageGraduateTime
                            }
                        ]
                    });
                },
                error => {
                    console.log(error)
                }
            )

        },
        tutorAssignChart(startDate, endDate){
            let tutorassignChart = this.$echarts.init(document.getElementById('tutorassignChart')) // 基于准备好的dom，初始化echarts实例

            // DONE: 从后端获取不同Week的分配新人数等数据
            var days = ['Week 9', 'Week 8', 'Week 7', 'Week 6', 'Week 5', 'Week 4', 'Week 3']
            var assignedNewcomers = [1400, 1300, 1200, 1250, 1150, 1250, 1350];
            var totalNewcomers = [2200, 2350, 2150, 2100, 2350, 2100, 2250];

            // 根据normalGraduate、totalGraduate计算出非正常毕业人数、正常毕业比例
            var unassignedNewcomers = [];
            var assignedNewcomersPercentage = []

            COMM.tutor_assignment_chart(startDate, endDate).then(
                response => {
                    console.log(response.data)
                    days = response.data.days
                    assignedNewcomers = response.data.assignedNewcomers
                    totalNewcomers = response.data.totalNewcomers
                    for(var i = 0; i < assignedNewcomers.length; i++){
                        unassignedNewcomers[i] = totalNewcomers[i] - assignedNewcomers[i];
                        assignedNewcomersPercentage[i] = Math.round(assignedNewcomers[i] / totalNewcomers[i] * 100);
                    }
                    tutorassignChart.setOption({
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                            type: 'shadow'
                            }
                        },
                        legend: {},
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                        },
                        xAxis: [
                            {
                            type: 'category',
                            data: days
                            }
                        ],
                        yAxis: [
                            {
                            type: 'value',
                            name: '人数',
                            min: 0,
                            axisLabel: {
                                formatter: '{value} 人'
                            }
                            },
                            {
                            type: 'value',
                            name: '百分比',
                            min: 0,
                            axisLabel: {
                                formatter: '{value}%'
                            }
                            }
                        ],
                        series: [
                            {
                            name: '已分配新人数',
                            type: 'bar',
                            yAxisIndex: 0,
                            emphasis: {
                                focus: 'series'
                            },
                            tooltip: {
                                valueFormatter: function (value) {
                                return value + ' 人';
                                }
                            },
                            data: assignedNewcomers 
                            },
                            {
                            name: '未分配新人数',
                            type: 'bar',
                            yAxisIndex: 0,
                            emphasis: {
                                focus: 'series'
                            },
                            tooltip: {
                                valueFormatter: function (value) {
                                return value + ' 人';
                                }
                            },
                            data: unassignedNewcomers
                            },
                            {
                            name: '导师分配率',
                            type: 'line',
                            yAxisIndex: 1,
                            emphasis: {
                                focus: 'series'
                            },
                            tooltip: {
                                valueFormatter: function (value) {
                                return value + '%';
                                }
                            },
                            data: assignedNewcomersPercentage
                            },
                        ]
                    });
                },
                error => {
                    console.log(error)
                }
            )

        }
    },
    watch: {
        "newcomerDateRange": {
            handler() {
                this.updateNewcomerAnalysis()
            }
        },
        "teacherDateRange": {
            handler() {
                this.updateTeacherAnalysis()
            }
        },
    },
    created() {
        var today = new Date()
        var endDate = new Date(today.toDateString())
        endDate.setDate(endDate.getDate() + 1)
        endDate.setMilliseconds(endDate.getMilliseconds() - 1)
        var startDate = new Date(today.toDateString())
        startDate.setDate(startDate.getDate() - 7)
        console.log("Init Date Range: ", startDate.toLocaleString(), endDate.toLocaleString())
        this.newcomerDateRange = [startDate, endDate]
        this.teacherDateRange = [startDate, endDate]
    }
})
</script>
