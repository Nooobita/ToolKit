# -*- coding=utf8 -*-


def bubble(alist):
    """冒泡排序O(n^2)"""
    n = len(alist)
    for j in range(n-1, 0, -1):
        for i in range(j):
            if alist[i] > alist[i+1]:
                alist[i], alist[i+1] = alist[i+1], alist[i]


def selection_sort(alist):
    """选择排序O(n^2)"""
    n = len(alist)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if alist[j] < alist[min_index]:
                min_index = j
        if min_index != i:
            alist[min_index], alist[i] = alist[i], alist[min_index]


def insert_sort(alist):
    """插入排序O(n^2)"""
    n = len(alist)
    for i in range(1, n):
        for j in range(i, 0, -1):
            if alist[j] < alist[j-1]:
                alist[j], alist[j-1] = alist[j-1], alist[j]


def quick_sort(alist):
    """快速排序O(n^2)"""
    if not alist:
        return []
    mid = alist[0]
    low = quick_sort([elem for elem in alist[1:] if elem < mid])
    high = quick_sort([elem for elem in alist[1:] if elem >= mid])
    return low + [mid] + high


def shell_sort(alist):
    """希尔排序O(n^2)"""
    n = len(alist)
    gap = n / 2

    while gap > 0:
        for i in range(gap, n):
            j = i
            while j >= gap and alist[j] < alist[j-gap]:
                alist[j], alist[j-gap] = alist[j-gap], alist[j]
        gap = gap / 2


def merge_sort(alist):
    """归并排序O(nlogn)"""
    if len(alist) <= 1:
        return alist

    mid = len(alist) / 2
    left = merge_sort(alist[:mid])
    right = merge_sort(alist[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    l, r = 0, 0
    while l < len(left) and r < len(right):
        if left[l] < right[r]:
            result.append(left[l])
            l += 1
        else:
            left[l] > right[r]
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result


def binary_search(alist, item):
    """二分查找法O(logn)"""
    if len(alist) == 0:
        return False
    else:
        mid_point = len(alist) // 2
        if alist[mid_point] == item:
            return True
        else:
            if alist[mid_point] < item:
                return binary_search(alist[mid_point+1:], item)
            else:
                return binary_search(alist[:mid_point], item)


if __name__ == '__main__':
    a = [1, 2, 3 ,4 ,5 ,6 ,7 ,8]
    print binary_search(a, 1)