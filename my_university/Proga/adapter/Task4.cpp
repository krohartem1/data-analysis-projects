/*
#include <string_view>
#include <string>
#include <iostream>
bool NextToken(std::string_view& sv, char delimiter, std::string_view& token)
{
    int pos = sv.find(delimiter);
    if (sv.size() != 0)
    {
        if (pos != -1) {
            token = sv.substr(0, pos);
            sv.remove_prefix(pos + 1);
        }
        else {
            token = sv.substr(0);
            sv.remove_prefix(sv.size());
        }
        return 1;
    }
    else { return 0; }
}

int main() {
    std::string_view sv = "Hello world and good bye";

    const char delimiter = ' ';
    std::string_view token;

    // Делим строку на токены по разделителю и перебираем эти токены:
    while (NextToken(sv, delimiter, token)) {
        // обрабатываем очередной token
        // например, печатаем его на экране:
        std::cout << token << "\n";
    }
    return 0;
}*/