package main

import (
	"fmt"
	"strings"
	"io/ioutil"
	"os"
	"strconv"
)
// Check if err
func check(e error) {
    if e != nil {
        panic(e)
    }
}
// Removing duplicated items
func unique(intSlice []string) []string {
    keys := make(map[string]bool)
    list := []string {}
    for _, entry := range intSlice {
        if _, value := keys[entry]; !value {
            keys[entry] = true
            list = append(list, entry)
        }
    }
    return list
}

// Pure functions
func leet(word string) string {
	return strings.NewReplacer("A","4", "E", "3", "I", "1", "O", "0", "S", "5", "T", "7", "B", "8").Replace(word)
}
func count1to8(word string) []string {
        list := []string {word}
        for i := 0; i < 9; i++ {
                list = append(list,list[len(list)-1]+strconv.Itoa(i))
        }
        return list
}
func year90(word string) []string {
        list := []string {word}
        for i := 99; i > 89; i-- {
                list = append(list,word+strconv.Itoa(i))
        }
        return list
}
func year2000(word string) []string {
        list := []string {word}
        for i := 2020; i > 1999; i-- {
                list = append(list,word+strconv.Itoa(i))
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
	runes := []rune(string(word))
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}
func mess(word string, allList []string) []string {
	list := []string {}
	for _, i := range allList {
		list = append(list, word + i)
	}
	return list
}
func combine(allList []string) []string {
	finalWords := []string {}

	for _, i := range allList {
		finalWords = append(finalWords, mess(i, allList)...)
	}

	return finalWords
}

func main() {
	finalContent := []string {}
	// Read base file
	blob, err := ioutil.ReadFile(os.Args[1])
	check(err)
	content := strings.Fields(string(blob))
	finalContent = append(content, combine(content)...)

	// Running functions for make wordlist
	for _, word := range content {
		finalContent = append(finalContent, leet(word))
		finalContent = append(finalContent, count1to8(word)...)
		finalContent = append(finalContent, year90(word)...)
		finalContent = append(finalContent, year2000(word)...)
		finalContent = append(finalContent, strings.ToUpper(word))
		finalContent = append(finalContent, strings.ToLower(word))
		finalContent = append(finalContent, strings.Map(swapCase, word))
		finalContent = append(finalContent, inverter(word))
	}

	// Save data
	file, errCreate := os.Create(os.Args[2])
	check(errCreate)
	defer file.Close()
	data := []byte(strings.Join(unique(finalContent), "\n"))
	numberWrote, errWrite := file.Write(data)
	check(errWrite)
	if numberWrote < 1 {
		fmt.Println("1b?")
	}
}
