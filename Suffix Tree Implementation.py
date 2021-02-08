class Node():
    def __init__(self, lable):
        self.lable = lable # lableel on path leading to this node
        self.edges = {}  # outgoing edges; maps characters to nodes

class SuffixTree():
    def __init__(self, s):
        s += '$'
        self.root = Node(None)
        self.root.edges[s[0]] = Node(s) 
        # add the rest of the suffixes, from longest to shortest
        for i in range(1, len(s)):
            current = self.root
            j = i
            while j < len(s):
                if s[j] in current.edges:
                    child = current.edges[s[j]]
                    lable = child.lable
                    # Walk along edge until we exhaust edge lable
                    k = j+1 
                    while k-j < len(lable) and s[k] == lable[k-j]:
                        k += 1
                    if k-j == len(lable):
                        current = child # we exhausted the edge
                        j = k
                    else:
                        # we fell off in middle of edge
                        child_Exist, New_child = lable[k-j], s[k]
                        # create “mid”: new node bisecting edge
                        mid = Node(lable[:k-j])
                        mid.edges[New_child] = Node(s[k:])
                        # original child becomes mid’s child
                        mid.edges[child_Exist] = child
                        # original child’s lableel is currenttailed
                        child.lable = lable[k-j:]
                        # mid becomes new child of original parent
                        current.edges[s[j]] = mid
                else:
                    # Fell off tree at a node: make new edge hanging off it
                    current.edges[s[j]] = Node(s[j:])

    def followPath(self, s):
        current = self.root
        i = 0
        while i < len(s):
            c = s[i]
            if c not in current.edges:
                return (None, None) # fell off at a node
            child = current.edges[s[i]]
            lable = child.lable
            j = i+1
            while j-i < len(lable) and j < len(s) and s[j] == lable[j-i]:
                j += 1
            if j-i == len(lable):
                current = child # exhausted edge
                i = j
            elif j == len(s):
                return (child, j-i) 
            else:
                return (None, None) # fell off in the middle of the edge
        return (current, None) 
    
    def hasSubstring(self, s):
        node, off = self.followPath(s)
        return node is not None
    
    def hasSuffix(self, s):
        node, off = self.followPath(s)
        if node is None:
            return False # fell off the tree
        if off is None:
            # finished on top of a node
            return '$' in node.edges
        else:
            return node.lable[off] == '$'

stree = SuffixTree('there would have been a time for such a word')
print(stree.hasSubstring('yes'))
print(stree.hasSubstring('would have been'))
print(stree.hasSubstring('such a word'))
print(stree.hasSuffix('would have been'))
print(stree.hasSuffix('such a word'))