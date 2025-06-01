def number_to_words(n):
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
             "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
             "Sixteen", "Seventeen", "Eighteen", "Nineteen"]

    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def get_words(num):
        if num < 20:
            return units[num]
        elif num < 100:
            return tens[num // 10] + (" " + units[num % 10] if num % 10 != 0 else "")
        else:
            return ""

    def convert(num):
        result = ""
        if num >= 10**7:
            result += get_words(num // 10**7) + " Crore "
            num %= 10**7
        if num >= 10**5:
            result += get_words(num // 10**5) + " Lakh "
            num %= 10**5
        if num >= 1000:
            result += get_words(num // 1000) + " Thousand "
            num %= 1000
        if num >= 100:
            result += get_words(num // 100) + " Hundred "
            num %= 100
        if num > 0:
            result += "and " + get_words(num) if result else get_words(num)
        return result.strip()

    ans = convert(n).replace("  ", " ") + " only."
    return ans[0].upper() + ans[1:].lower()


        