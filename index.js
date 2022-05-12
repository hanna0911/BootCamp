const http = require('http')

const app = require('./dist')
// const db = require('./db')

// db.migrate.latest()

var server = http.createServer(app)

server.listen(process.env.SERVER_PORT || 3000, function () {
  const host = server.address().address
  const port = server.address().port
  console.log('listening at http://%s:%s', host, port)
})

