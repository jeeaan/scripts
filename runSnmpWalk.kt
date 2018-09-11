   suspend fun runSnmpWalk(ip : String, code : String) : String {
        var result = awaitBlocking {
            try {
                val process = ProcessBuilder("snmpwalk", "-v", "1", "-c", "private", ip, code).start()
                val result = process.inputStream.reader(Charsets.UTF_8).use { it.readText() }
                        .replace("\"", "")
                        .split(":")
                result[1]

            } catch (e: Exception) {
                throw e
                "Erro ao rodar snmpwalk"
            }
        }
        return result.trim()
    }