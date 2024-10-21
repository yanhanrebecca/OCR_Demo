import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: () => import('@/views/login/index.vue')
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/views/home/index.vue'),
      children: [
        {
          path:'/manager',
          name:'caseManager',
          component: () => import('@/views/case/manager/index.vue')
        },
        {
          path:'/edit/:id',
          name:'caseEdit',
          component: () => import('@/views/case/edit/index.vue')
        },
        {
          path:'/create',
          name:'caseCreate',
          component: () => import('@/views/case/create/index.vue')
        },
        // {
        //   path:'/test',
        //   name:'caseTest',
        //   component: () => import('@/views/case/test/index.vue')
        // }


      ]
    }
  ]
})

export default router
