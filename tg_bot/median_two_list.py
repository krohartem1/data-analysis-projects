def findMedianSortedArrays(nums1, nums2):
    left1, right1, left2, right2 = 0, len(nums1), 0, len(nums2)
    n = len(nums1) + len(nums2)
    median_left_elem = -1
    while left1 < right1 and left2 < right2:
        mid1 = (left1 + right1) // 2
        mid2 = (left2 + right2) // 2
        if mid1 + mid2 + 2 > (n + 1) // 2:
            if nums1[mid1] >= nums2[mid2]:
                right1 = mid1
            else:
                right2 = mid2
        else:
            if nums1[mid1] <= nums2[mid2]:
                left1 = mid1 + 1
            else:
                left2 = mid2 + 1

    if left1 == right1:
        left2 = (n + 1) // 2 - left1
        median_left_elem = nums2[(n + 1) // 2 - left1 - 1]
    else:
        left1 = (n + 1) // 2 - left2
        median_left_elem = nums1[(n + 1) // 2 - left2 - 1]

    if n % 2 == 1:
        return median_left_elem
    else:
        if left1 < len(nums1) and left2 < len(nums2):
            return (median_left_elem + min(nums1[left1], nums2[left2])) / 2
        elif left1 >= len(nums1) and left2 < len(nums2):
            return (median_left_elem + nums2[left2]) / 2
        else:
            return (median_left_elem + nums1[left1]) / 2


ans = findMedianSortedArrays([0, 0], [0, 0])
print(ans)
