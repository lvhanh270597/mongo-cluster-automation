db = connect("mongodb://localhost:27019/admin")

db.createUser({ user: "admin", pwd: "Xfam0usx", roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }
 ]})