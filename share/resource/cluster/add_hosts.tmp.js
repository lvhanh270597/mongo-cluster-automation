db = connect("mongodb://localhost:27019/admin")
db.auth("admin", "Xfam0usx")

hosts = ['172.16.176.131:27019', '172.16.176.132:27019']
for (var i=0; i<hosts.length; i++){
  rs.add({_id: i + 1, host: hosts[i]})
}