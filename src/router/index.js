import Vue from 'vue'
import VueRouter from 'vue-router'
// import App from '@/App.vue'
import NewcomerManage from '@/components/NewcomerManage.vue'
import TutorManage from '@/components/TutorManage.vue'
import TrainTemplate from '@/components/TrainTemplate.vue'
import NewcomerBoard from '@/components/NewcomerBoard.vue'
// import TrainNotice from '@/components/TrainNotice.vue' // 暂时隐藏掉
// import HelpPage from '@/components/HelpPage.vue'
// import WelcomePage from "@/components/WelcomePage";
import DimensionAnalysis from "@/components/DimensionAnalysis.vue";
import VideoDispalyTest from "@/components/VideoDispalyTest";
import LeadNewcomer from "@/components/LeadNewcomer.vue"
import TutorTrain from "@/components/TutorTrain.vue"
import PersonalProfile from "@/components/PersonalProfile.vue"
import CommitDialog from "@/components/subcomponents/CommitDialog";
import RecodeDialog from "@/components/subcomponents/RecodeDialog";
import CreateNotification from "@/components/CreateNotification.vue"
import ReadNotification from "@/components/ReadNotification.vue"
import CommitAndScoreDialog from "@/components/subcomponents/commitAndScoreDialog";
import jumpBack from "@/components/subcomponents/jumpBack";

Vue.use(VueRouter)

const routes = [
	// TODO：后期重新配一下路由，先把/的注释掉，这样避免回退网页的问题（直接暴力禁止访问。。。
	// {
	// 	path: '/',
	// 	name: 'App',
	// 	component: App,
	// },
	{
		path: '/newcomer-manage',
		name: 'NewcomerManage',
		component: NewcomerManage,
		meta: { requireAuth: true }  // 验证cookie，通过后才允许跳转，否则回登录页
	},
	{
		path: '/tutor-manage',
		name: 'TutorManage', 
		component: TutorManage,
		meta: { requireAuth: true }
	},
	{
		path: '/train-template',
		name: 'TrainTemplate',
		component: TrainTemplate,
		meta: { requireAuth: true }
	},
	{
		path: '/newcomer-board',
		name: 'NewcomerBoard',
		component: NewcomerBoard,
		meta: { requireAuth: true }
	},
	// 暂时隐藏掉
	// {
	// 	path: '/train-notice',
	// 	name: 'TrainNotice',
	// 	component: TrainNotice,
	// 	meta: { requireAuth: true }
	// },
	// {
	// 	path: '/help-page',
	// 	name: 'HelpPage',
	// 	component: HelpPage,
	// 	meta: { requireAuth: true }
	// },
	// {
	// 	path:"/welcome",
	// 	name:"Welcome",
	// 	component: WelcomePage,
	// 	meta: {requireAuth: true}
	// },
	{
		path: '/dimension-analysis',
		name: 'DimensionAnalysis',
		component: DimensionAnalysis,
		meta: { requireAuth: true }
	},
	{
		path: '/video-test',
		name:"VideoDisplayTest",
		component: VideoDispalyTest,
		meta : {requireAuth: true}
	},
	{
		path: '/lead-newcomer',
		name: 'LeadNewcomer',
		component: LeadNewcomer,
		meta: { requireAuth: true }
	},
	{
		path: '/tutor-train',
		name: 'TutorTrain',
		component: TutorTrain,
		meta: { requireAuth: true }
	},
	{
		path: '/',
		name: 'PersonalProfile',
		component: PersonalProfile,
		meta: { requireAuth: true }
	},
	{
		path: '/commitdialog',
		name: 'commitDialog',
		component: CommitDialog,
		meta: { requireAuth: true }
	},
	{
		path: '/recode',
		name: 'recodeDialog',
		component: RecodeDialog,
		meta: { requireAuth: true }
	},
	{
		path: '/create-notification',
		name: 'createNotification',
		component: CreateNotification,
		meta: { requireAuth: true }
	},
	{
		path: '/read-notification',
		name: 'readNotification',
		component: ReadNotification,
		meta: { requireAuth: true }
	},
	{
		path: '/cas',
		name: 'CommitAndScoreDialog',
		component: CommitAndScoreDialog,
		meta: { requireAuth: true }
	},
	{
		path: "/jumpBack",
		name: "jumpBack",
		component: jumpBack,
		meta: {requireAuth:true}
	},
	// TODO
	{
		path: "*",
		redirect: "/"
	}
]

const router = new VueRouter({
	mode: 'history',
	routes
})

export default router