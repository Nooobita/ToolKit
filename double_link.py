# -*- coding=utf8 -*-


class Node(object):
    """节点类"""
    def __init__(self, elem):
        self.pre = None
        self.next = None
        self.elem = elem


class Double_Link(object):
    """双向链表"""
    def __init__(self):
        self.__head = None

    def is_empty(self):
        """链表是否为空"""
        return self.__head is None

    def length(self):
        """链表长度"""
        count = 0
        cur = self.__head
        while cur is not None:
            cur = cur.next
            count += 1
        return count

    def travel(self):
        """遍历链表"""
        cur = self.__head
        while cur is not None:
            print cur.elem,
            cur = cur.next

    def add(self, elem):
        """链表头部添加"""
        node = Node(elem)
        cur = self.__head
        self.__head = node
        if cur:
            node.next = cur
            cur.pre = node

    def append(self, elem):
        """链表尾部添加"""
        node = Node(elem)
        cur = self.__head
        while cur.next is not None:
            cur = cur.next
        cur.next = node
        node.pre = cur

    def insert(self, pos, elem):
        """指定位置添加"""
        node = Node(elem)
        if pos <= 0:
            self.add(elem)
        elif pos >= (self.length() - 1):
            self.append(elem)
        else:
            count = 0
            cur = self.__head
            while cur is not None and count != pos:
                cur = cur.next
                count += 1
            cur.pre.next = node
            node.pre = cur.pre
            node.next = cur
            cur.pre = node

    def remove(self, elem):
        """删除节点"""
        if self.is_empty():
            return
        cur = self.__head
        if cur.elem == elem:
            if cur.next is None:
                self.__head = None
            else:
                cur.next.pre = None
                self.__head = cur.next
            return

        while cur.next is not None:
            if cur.elem == elem:
                cur.pre.next = cur.next
                cur.next.pre = cur.pre
                return
            cur = cur.next
        # 最后一个节点
        if cur.elem == elem:
            cur.pre.next = None

    def search(self, elem):
        """查找节点是否存在"""
        cur = self.__head
        while cur is not None:
            if cur.elem == elem:
                return True
            cur = cur.next
        return False

if __name__ == '__main__':
    double = Double_Link()
    double.add(1)
    double.add(2)
    double.add(3)
    double.append(4)
    double.travel()
    print ""
    double.insert(2, 100)
    double.remove(3)
    double.travel()