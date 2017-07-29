# -*- coding=utf8 -*-


class Node(object):
    """节点类"""
    def __init__(self, elem):
        self.elem = elem
        self.next = None


class SingleLink(object):
    """单链表类"""
    def __init__(self):
        self.__head = None

    def is_empty(self):
        """链表是否为空"""
        return  self.__head is None

    def length(self):
        """链表长度"""
        count = 0

        node = self.__head
        while node is not None:
            count += 1
            node = node.next
        return count

    def travel(self):
        """遍历整个链表"""
        node = self.__head
        while node is not None:
            print node.elem,
            node = node.next

    def add(self, elem):
        """链表头部添加元素"""
        node = Node(elem)
        node.next = self.__head
        self.__head = node

    def append(self, elem):
        """链表尾部添加元素"""
        elem = Node(elem)
        node = self.__head
        # 先判断链表是否为空，若是空链表，则将_head指向新节点
        if node is None:
            self.__head = elem
        # 若不为空，则找到尾部，将尾节点的next指向新节点
        else:
            while node.next is not None:
                node = node.next
            node.next = elem

    def insert(self, pos, elem):
        """指定位置添加元素"""
        item = Node(elem)
        node = self.__head
        count = 0
        pre = None
        # 若指定位置pos为第一个元素之前，则执行头部插入
        if pos <= 0:
            self.add(elem)
        # 若指定位置超过链表尾部，则执行尾部插入
        elif pos > (self.length()-1):
            self.append(elem)
        else:
            while node is not None and count != pos:
                pre = node
                node = node.next
                count += 1
            pre.next = item
            item.next = node

    def remove(self, elem):
        """删除节点"""
        node = self.__head
        pre = None
        if node is None:
            return
        while node is not None:
            if node.elem == elem:
                if not pre:
                    self.__head = node.next
                else:
                    pre.next = node.next
                break
            else:
                pre = node
                node = node.next

    def search(self, elem):
        """查找节点是否存在"""
        node = self.__head
        while node is not None:
            if node.elem == elem:
                return True
            node = node.next
        return False

if __name__ == '__main__':
    single = SingleLink()
    print single.is_empty()
    single.add(4)
    single.add(5)
    single.add(8)
    # single.append(11)
    print single.length()
    single.remove(5)
    single.travel()