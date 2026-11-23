package com.zedempires.zarmakeyboard

object ZarmaDictionary {
    val WORDS = listOf(
        "\uE014\uE002\uE01F\uE002", "\uE016\uE009\uE015\uE002", "\uE017\uE002\uE01F\uE029\uE002",
        "\uE01A\uE000\uE014\uE003", "\uE016\uE007\uE017\uE000\uE022", "\uE01B\uE000\uE02B\uE020\uE000\uE02B\uE014\uE004\uE02E",
        "\uE01D\uE002\uE023\uE000\uE015\uE001\uE02E", "\uE01C\uE000\uE01F\uE017\uE004\uE02E", "\uE01E\uE000\uE021\uE001\uE02E",
        "\uE020\uE000\uE01C\uE014\uE000\uE02E", "\uE021\uE000\uE005\uE016\uE001\uE02E", "\uE028\uE000\uE022",
        "\uE024\uE007\uE01A\uE000", "\uE029\uE000\uE02B\uE01F\uE001", "\uE025\uE000\uE02B",
        "\uE027\uE000\uE014\uE005", "\uE020\uE007\uE015\uE005", "\uE01C\uE001\uE02B\uE01B\uE000\uE02E",
        "\uE023\uE000\uE02B\uE01C\uE002", "\uE000\uE016\uE002", "\uE001\uE018\uE008\uE01A\uE000",
        "\uE001\uE018\uE008\uE024\uE000", "\uE001\uE021\uE000\uE027\uE001", "\uE001\uE017\uE004",
        "\uE001\uE015\uE004", "\uE001\uE023\uE003", "\uE001\uE018\uE000\uE01A\uE004",
        "\uE001\uE023\uE003\uE017\uE000", "\uE024\uE007\uE017\uE004", "\uE024\uE000\uE01C\uE014\uE000\uE01F",
        "\uE018\uE000\uE022\uE000\uE01F\uE001"
    )
    fun suggest(prefix: String): List<String> {
        if (prefix.isEmpty()) return listOf("\uE014\uE002\uE01F\uE002", "\uE024\uE007\uE01A\uE000", "\uE016\uE009\uE015\uE002")
        val matches = WORDS.filter { it.startsWith(prefix) && it != prefix }.take(3).toMutableList()
        if (matches.size < 3) matches.add(prefix + "\uE02C")
        if (matches.size < 3) matches.add(prefix + "\uE02E")
        return matches.take(3)
    }
}
