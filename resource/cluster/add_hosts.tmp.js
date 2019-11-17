db = connect("mongodb://localhost:27017/admin")
db.auth("admin", "password")

hosts = ['172.16.176.131', '172.16.176.132']
for (var i=0; i<hosts.length; i++){
  rs.add({_id: i + 1, host: hosts[i]})
}