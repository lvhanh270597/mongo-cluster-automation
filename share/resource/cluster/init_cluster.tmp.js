db = connect("mongodb://localhost:27019/admin")

db.auth("admin", "Xfam0usx")

rs.initiate(
    {
      _id: "test_repl",
      members: [
        { _id : 0, host : "172.16.176.130:27019" }
      ]
    }
)
