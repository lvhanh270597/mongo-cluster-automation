db = connect("mongodb://localhost:27017/admin")

db.createUser({ user: "admin", pwd: "password", roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
 ]})