import axios from 'axios'

const url = 'http://127.0.0.1:5000'

// 创建axios实例
const service = axios.create({
  baseURL: url
})

// request拦截器
service.interceptors.request.use(
  config => {
    var Authorization = window.sessionStorage.getItem('Authorization')
    config.headers.Authorization = Authorization
    if (config.headers['Content-Type'] === 'multipart/form-data' || config.method !== 'post') {
      return config
    }
    // config.data = qs.stringify(config.data)

    return config
  },
  error => {
    Promise.reject(error)
  }
)

// response 拦截器
service.interceptors.response.use(
  response => {
    return response
  },
  error => {
    return Promise.reject(error)
  }
)

export { url }

export function register (data) {
  return service({
    url: '/user/register',
    method: 'post',
    data
  })
}

export function login (data) {
  return service({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function recover (params) {
  return service({
    url: '/user/recover',
    method: 'get',
    params
  })
}

export function userInfo (params) {
  return service({
    url: '/user/info',
    method: 'get',
    params
  })
}

export function processFile (data) {
  return service({
    url: '/user/process',
    method: 'post',
    data
  })
}

export function getFile (params) {
  return service({
    url: '/user/download',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

export function getClients (params) {
  return service({
    url: '/user/clients',
    method: 'get',
    params
  })
}

export function getIncomes (params) {
  return service({
    url: '/client/incomes',
    method: 'get',
    params
  })
}
