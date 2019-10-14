import Layout from '@/layout'

const userRouter = {
    path: '/usermanage',
    component: Layout,
    redirect: '/usermanage/user',
    name: 'usermanage',
    meta: {
        title: '用户管理',
        icon: 'user'
    },
    children: [
        {
            path: 'user',
            component: () => import('@/views/usermanage/user'),
            name: 'user',
            meta: { title: '用户列表' }
        },
        {
            path: 'functions',
            component: () => import('@/views/usermanage/functions'),
            name: 'functions',
            meta: { title: '权限列表' }
        }
    ]
}
export default userRouter