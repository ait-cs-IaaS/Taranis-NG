const fs = require('fs')
const path = require('path')

const configPath = path.join(__dirname, '../dist/config.json')
const gitInfoPath = path.join(__dirname, '../dist/git_info.json')
const configJson = require(configPath)
const gitInfo = require(gitInfoPath)
configJson.BUILD_DATE = new Date().toISOString()
configJson.GIT_INFO = gitInfo
fs.writeFileSync(configPath, JSON.stringify(configJson, null, 2))
