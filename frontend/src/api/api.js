import axios from 'axios'
// import qs from 'qs'

const url = 'http://0.0.0.0:5000'

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
    data: data
  })
}


export function login (data) {
  return service({
    url: '/user/login',
    method: 'post',
    data: data
  })
}


export function findByUsername (params) {
  return service({
    url: '/user/username',
    method: 'get',
    params: params
  })
}


export function addClient (data) {
  return service({
    url: '/client/add',
    method: 'post',
    data: data
  })
}


export function getIncomeByUser (data) {
  return service({
    url: '/client/incomes',
    method: 'get',
    data: data
  })
}


export function findAllClients (params) {
  return service({
    url: '/user/clients',
    method: 'get',
    params: params
  })
}
