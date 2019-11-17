db = connect("mongodb://localhost:27017/cmdb")

db.createUser({ user: "cmdb", pwd: "password", roles: [
    { role: "readWrite", db: "cmdb" },
 ]})