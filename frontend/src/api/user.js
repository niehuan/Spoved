import request from '@/utils/request'

//登录验证，获取token
export function login(data) {
  return request({
    baseURL: 'http://127.0.0.1:8000/api',
    url: '/user/login/',
    method: 'post',
    data

  })
}

//根据token获取用户信息
export function getInfo(token) {
  return request({
    baseURL: 'http://127.0.0.1:8000/api',
    url: '/user/info/',
    method: 'get',
    params: { token }
  })
}

// export function logout() {
//   return request({
//     url: '/user/logout/',
//     method: 'post'
//   })
// }

//获取用户列表
export function getuserlist(query) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/user/',
        method: 'get',
        params: query

    })
}

//创建用户
export function createUser(data) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/user/',
        method: 'post',
        data
    })

}

//删除用户
export function delUser(data) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/user/',
        method: 'delete',
        data
    })
}

//更新用户
export function updateUser(data) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/user/',
        method: 'put',
        data
    })
}

//获取用户后端权限列表
export function getFuncslist(query) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/func/',
        method: 'get',
        params: query
    })
}

//获取后端所有权限列表
export function getFuncAll(query) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/func_all/',
        method: 'get',
        params: query
    })
}

//获取后端所有用户列表
export function getUserAll(query) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/user_all/',
        method: 'get',
        params: query
    })
}

//新增权限
export function createFunc(data) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/func/',
        method: 'post',
        data
    })
}

//修改权限
export function updateFunc(data) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/func/',
        method: 'put',
        data
    })

}

//删除权限
export function delFunc(data) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/func/',
        method: 'delete',
        data
    })
}

//获取角色
export function getRoleslist(query) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/role/',
        method: 'get',
        params: query
    })
}

//添加或修改角色所拥有的权限
export function createRolePerms(data) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/role_func/',
        method: 'post',
        data
    })
}

export function createRoleUsers(data) {
    return request({
        baseURL: 'http://127.0.0.1:8000/api',
        url: '/mg/accounts/role_user/',
        method: 'post',
        data
    })
}