# -*- coding=utf8 -*-


class Node(object):
    """节点类"""
    def __init__(self, elem):
        self.elem = elem
        self.next = None


class SingleCircularLink(object):
    """单循环链表"""
    def __init__(self):
        self.__head = None

    def is_empty(self):
        """判断链表是否为空"""
        return self.__head is None

    def length(self):
        """返回链表的长度"""

        if self.is_empty():
            return 0
        count = 1
        node = self.__head
        while node.next != self.__head:
            count += 1
            node = node.next
        return count

    def travel(self):
        """遍历"""
        if self.is_empty():
            return
        node = self.__head
        print node.elem,
        while node.next != self.__head:
            node = node.next
            print node.elem,

    def add(self, elem):
        """在头部添加一个节点"""

        node = Node(elem)
        if self.is_empty():
            self.__head = node
            node.next = self.__head
        else:
            cur = self.__head
            node.next = cur
            # 找到最后一个元素指向头元素
            while cur.next != self.__head:
                cur = cur.next
            cur.next = node
            self.__head = node

    def append(self, elem):
        """在尾部添加一个节点"""
        node = Node(elem)
        if self.is_empty():
            self.__head = node
            node.next = self.__head
        else:
            cur = self.__head
            while cur.next != self.__head:
                cur = cur.next
            cur.next = node
            node.next = self.__head

    def insert(self, pos, elem):
        """在指定位置pos添加节点"""
        node = Node(elem)
        if pos <= 0:
            self.add(elem)
        elif pos >= (self.length() - 1):
            self.append(elem)
        else:
            count = 1
            pre = None
            cur = self.__head
            while cur.next != self.__head and count != (pos+1):
                pre = cur
                cur = cur.next
                count += 1
            pre.next = node
            node.next = cur

    def remove(self, elem):
        """删除一个节点"""
        if self.is_empty():
            return
        cur = self.__head
        pre = None
        # 删除第一个
        if cur.elem == elem:
            # 找到最后一个元素，更改头节点
            while cur.next != self.__head:
                pre = cur
                cur = cur.next
            if pre is None:
                self.__head = None
            else:
                self.__head = self.__head.next
                cur.next = self.__head
        # 删除非第一个元素
        else:
            while cur.next != self.__head:
                pre = cur
                cur = cur.next
                if cur.elem == elem:
                    pre.next = cur.next
                    return
            # 如果为最后一个
            if cur.elem == elem:
                pre.next = self.__head

    def search(self, elem):
        """查找节点是否存在"""
        if self.is_empty():
            return False
        cur = self.__head
        if cur.elem == elem:
            return True
        while cur.next != self.__head:
            cur = cur.next
            if cur.elem == elem:
                return True
        return False

if __name__ == '__main__':
    single = SingleCircularLink()
    single.add(10)
    # single.add(9)
    # single.add(8)
    # single.append(100)
    # single.append(777)
    # single.insert(2, 22)
    single.travel()
    print ""
    single.remove(10)
    single.travel()
    # print single.length()
