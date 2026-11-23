package com.zedempires.zarmakeyboard

object ZarmaDictionary {
    val WORDS = listOf(
        "\uE814\uE802\uE81F\uE802", "\uE816\uE809\uE815\uE802", "\uE817\uE802\uE81F\uE829\uE802",
        "\uE81A\uE800\uE814\uE803", "\uE816\uE807\uE817\uE800\uE822", "\uE81B\uE800\uE82B\uE820\uE800\uE82B\uE814\uE804\uE82E",
        "\uE81D\uE802\uE823\uE800\uE815\uE801\uE82E", "\uE81C\uE800\uE81F\uE817\uE804\uE82E", "\uE81E\uE800\uE821\uE801\uE82E",
        "\uE820\uE800\uE81C\uE814\uE800\uE82E", "\uE821\uE800\uE805\uE816\uE801\uE82E", "\uE828\uE800\uE822",
        "\uE824\uE807\uE81A\uE800", "\uE829\uE800\uE82B\uE81F\uE801", "\uE825\uE800\uE82B",
        "\uE827\uE800\uE814\uE805", "\uE820\uE807\uE815\uE805", "\uE81C\uE801\uE82B\uE81B\uE800\uE82E",
        "\uE823\uE800\uE82B\uE81C\uE802", "\uE800\uE816\uE802", "\uE801\uE818\uE808\uE81A\uE800",
        "\uE801\uE818\uE808\uE824\uE800", "\uE801\uE821\uE800\uE827\uE801", "\uE801\uE817\uE804",
        "\uE801\uE815\uE804", "\uE801\uE823\uE803", "\uE801\uE818\uE800\uE81A\uE804",
        "\uE801\uE823\uE803\uE817\uE800", "\uE824\uE807\uE817\uE804", "\uE824\uE800\uE81C\uE814\uE800\uE81F",
        "\uE818\uE800\uE822\uE800\uE81F\uE801"
    )
    fun suggest(prefix: String): List<String> {
        if (prefix.isEmpty()) return listOf("\uE814\uE802\uE81F\uE802", "\uE824\uE807\uE81A\uE800", "\uE816\uE809\uE815\uE802")
        val matches = WORDS.filter { it.startsWith(prefix) && it != prefix }.take(3).toMutableList()
        if (matches.size < 3) matches.add(prefix + "\uE82C")
        if (matches.size < 3) matches.add(prefix + "\uE82E")
        return matches.take(3)
    }
}
