package tests

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func mergeSort(arr []int) []int {
	if len(arr) <= 1 {
		return arr
	}

	mid := len(arr) / 2
	left := mergeSort(arr[:mid])
	right := mergeSort(arr[mid:])
	return merge(left, right)
}

func merge(left, right []int) []int {
	result := []int{}
	i, j := 0, 0

	for i < len(left) && j < len(right) {
		if left[i] < right[j] {
			result = append(result, left[i])
			i++
		} else {
			result = append(result, right[j])
			j++
		}
	}

	// Equivalent short code
	// return append(result, append(left[i:], right[j:]...)...)

	for i < len(left) {
		result = append(result, left[i])
		i++
	}

	for j < len(right) {
		result = append(result, right[j])
		j++
	}

	return result
}

func Test_mergeSort(t *testing.T) {
	fixture := []int{4, 2, 7, 1, 0}
	expected := []int{0, 1, 2, 4, 7}

	result := mergeSort(fixture)

	assert.Equal(t, expected, result)
	fmt.Println(result)
}
