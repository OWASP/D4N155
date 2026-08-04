package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"strconv"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func leet(word string) string {
	return strings.NewReplacer(
		"A", "4", "E", "3", "I", "1", "O", "0", "S", "5", "T", "7", "B", "8",
		"a", "4", "e", "3", "i", "1", "o", "0", "s", "5", "t", "7", "b", "8",
	).Replace(word)
}

func count1to8(word string) []string {
	list := []string{word}
	for i := 0; i < 9; i++ {
		list = append(list, list[len(list)-1]+strconv.Itoa(i))
	}
	return list
}

func year90(word string) []string {
	list := []string{word}
	for i := 99; i > 89; i-- {
		list = append(list, word+strconv.Itoa(i))
	}
	return list
}

func year2000(word string) []string {
	list := []string{word}
	for i := 2026; i > 1999; i-- {
		list = append(list, word+strconv.Itoa(i))
	}
	return list
}

func swapCase(r rune) rune {
	switch {
	case 'a' <= r && r <= 'z':
		return r - 'a' + 'A'
	case 'A' <= r && r <= 'Z':
		return r - 'A' + 'a'
	default:
		return r
	}
}

func inverter(word string) string {
	runes := []rune(word)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func combine(list []string) []string {
	final := make([]string, 0, len(list)*len(list))
	for _, a := range list {
		for _, b := range list {
			final = append(final, a+b)
		}
	}
	return final
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Uso: GoMutation <input-file> <output-file>")
		os.Exit(1)
	}
	inputPath := os.Args[1]
	outputPath := os.Args[2]

	inFile, err := os.Open(inputPath)
	check(err)
	defer inFile.Close()

	scanner := bufio.NewScanner(inFile)
	scanner.Split(bufio.ScanWords)

	content := []string{}
	for scanner.Scan() {
		t := scanner.Text()
		if t != "" {
			content = append(content, t)
		}
	}
	check(scanner.Err())

	outFile, err := os.Create(outputPath)
	check(err)
	defer outFile.Close()

	writer := bufio.NewWriter(outFile)
	defer func() {
		check(writer.Flush())
	}()

	seen := make(map[string]struct{})

	emit := func(s string) {
		if s == "" {
			return
		}
		if _, ok := seen[s]; ok {
			return
		}
		seen[s] = struct{}{}
		_, err := writer.WriteString(s + "\n")
		check(err)
	}

	processWordVariants := func(word string) {
		emit(word)
		emit(leet(word))

		for _, v := range count1to8(word) {
			emit(v)
		}
		for _, v := range year90(word) {
			emit(v)
		}
		for _, v := range year2000(word) {
			emit(v)
		}

		emit(strings.ToUpper(word))
		emit(strings.ToLower(word))
		emit(strings.Map(swapCase, word))
		emit(inverter(word))
	}

	for _, w := range content {
		processWordVariants(w)
	}

	for i := 0; i < len(content); i++ {
		for j := 0; j < len(content); j++ {
			comb := content[i] + content[j]
			processWordVariants(comb)
		}
	}

}
