import { app } from '../main.js'

export function xorConcat(array, element) {
  const i = array.indexOf(element)
  if (i === -1) {
    array.push(element)
  } else {
    array.splice(i, 1)
  }
  return array
}

export function isValidUrl(urlString) {
  var urlPattern = new RegExp(
    '^(https?:\\/\\/)?' + // validate protocol
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // validate domain name
      '((\\d{1,3}\\.){3}\\d{1,3}))' + // validate OR ip (v4) address
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // validate port and path
      '(\\?[;&a-z\\d%_.~+=-]*)?' + // validate query string
      '(\\#[-a-z\\d_]*)?$',
    'i'
  ) // validate fragment locator
  return !!urlPattern.test(urlString)
}

export function stripHtml(html) {
  const tmp = document.createElement('DIV')
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ''
}

export function notifySuccess(text) {
  app.$emit('notification', {
    type: 'success',
    loc: text
  })
}

export function notifyFailure(text) {
  app.$emit('notification', {
    type: 'red',
    loc: text
  })
}

export function emptyValues(obj) {
  const result = {}
  for (const key of Object.keys(obj)) {
    const value = obj[key]
    if (typeof value === 'string') {
      result[key] = ''
    } else if (Array.isArray(value)) {
      result[key] = []
    } else if (typeof value === 'object') {
      result[key] = emptyValues(value)
    } else {
      result[key] = undefined
    }
  }
  return result
}

export function objectFromFormat(format) {
  var newObject = {}
  format.map(function (item) {
    if (item === undefined) {
      return
    }
    if (item.type === 'checkbox') {
      newObject[item.name] = false
    } else if (
      item.type === 'text' ||
      item.type === 'textarea' ||
      item.type === 'select'
    ) {
      newObject[item.name] = ''
    } else if (item.type === 'number') {
      newObject[item.name] = 0
    } else if (item.type === 'table') {
      newObject[item.name] = []
    }
  })
  return newObject
}

export function parseParameterValues(data) {
  const sources = []

  data.forEach((source) => {
    const rootLevel = source

    source.parameter_values.forEach((parameter) => {
      rootLevel[parameter.parameter.key] = parameter.value
    })
    sources.push(rootLevel)
  })

  return sources
}

export function parseSubmittedParameterValues(unparsed_sources, data) {
  const result = unparsed_sources.find((item) => item.id === data.id)

  result.parameter_values.forEach((parameter) => {
    parameter.value = data[parameter.parameter.key]
  })

  return result
}

export function createParameterValues(parameters, data) {
  data.parameter_values = parameters.map((param) => ({
    parameter: param,
    value: data[param] || ''
  }))
  return data
}

export function tagIconFromType(tag_type) {
  if (tag_type === 'ORG') {
    return 'mdi-domain'
  }
  if (tag_type === 'LOC') {
    return 'mdi-map-marker'
  }
  if (tag_type === 'PER') {
    return 'mdi-account'
  }
  return 'mdi-tag'
}

export function tagTextFromType(tag_type) {
  if (tag_type === 'ORG') {
    return 'Organization'
  }
  if (tag_type === 'LOC') {
    return 'Location'
  }
  if (tag_type === 'PER') {
    return 'Person'
  }
  return 'Miscellaneous'
}
