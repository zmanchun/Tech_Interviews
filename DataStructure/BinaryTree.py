''' Implement a binary tree
'''

from collections import deque
class Node(object):
    def __init__(self,data):
        self.data=data
        self.left=None
        self.right=None
        self.parent=None
    
    def __repr__(self):
        return '%s(%r)' %(self.__class__.__name__, self.data)

class BinaryTree(object):
    def __init__(self, root = None):
        self.root=root
        self.child_dict={}
    
    def __repr__(self):
        return '%s(%r)' %(self.__class__.__name__, self.root)
        
    #use pre_order and in_order sequence to recursively create the binary tree
    def create_tree(self,pre_order,in_order):
        if len(pre_order)==0:
            return None
        n=Node(pre_order[0])
        pos=in_order.index(pre_order[0])
        n.left=self.create_tree(pre_order[1:pos+1],in_order[:pos])
        if n.left!=None:
            n.left.parent=n
        n.right=self.create_tree(pre_order[pos+1:], in_order[pos+1:])
        if n.right!=None:
            n.right.parent=n
        self.root=n
        return n
        
    def pre_order_print(self,r):
        if r:
            print r.data,
            self.pre_order_print(r.left)
            self.pre_order_print(r.right)
        
    def in_order_print(self,r):
        if r:
            self.in_order_print(r.left)
            print r.data,
            self.in_order_print(r.right)
    
    def post_order_print(self,r):
        if r:
            self.post_order_print(r.left)
            self.post_order_print(r.right)
            print r.data,
    
    def pre_order_printNR(self,r):
        'use stack, push root, if right not none, push right, if left not none, push left'
        stack=[]
        stack.append(r)
        while stack:    #python way to check if a list is not empty
            print stack[-1].data,
            p=stack[-1]
            stack.pop()
            if p.right!=None:
                stack.append(p.right)
            if p.left!=None:
                stack.append(p.left)
    
    def in_order_printNR(self,r):
        'go to the leftmost then go to the right subtree'
        stack=[]
        current=r
        while current or stack:
            if current:
                stack.append(current)
                current=current.left
            else:
                current=stack.pop()
                print current.data,
                current=current.right    
    
    def level_order_print(self,r):
        queue=deque([])
        level_no=deque([])
        queue.append(r)
        level_no.append(1)
        while queue:
            p=queue.popleft()
            level=level_no.popleft()
            print level,':', p.data
            if p.left:
                queue.append(p.left)
                level_no.append(level+1)
            if p.right:
                queue.append(p.right) 
                level_no.append(level+1)
    
    def get_height(self,r):
        if not r:
            return 0
        left_height=self.get_height(r.left)
        right_height=self.get_height(r.right)
        if left_height>right_height:
            return 1+left_height
        else:
            return 1+right_height
    
    def get_loweset_ancestor(self,r,x1,x2):
        if not self.is_find(r,x1) or not self.is_find(r, x2):
            print 'Cannot find x1 or x2. Invalid Input'
        ''' Two stop conditions:
                x1, x2 are in the different subtree of r
                (r.data, x1) or (r.data, x2) is not in the dictionary, this can only happen
                when the x1 is the direct ancestor of x2 or vice versa 
        '''
        while (r.data,x1) in self.child_dict and (r.data,x2) in self.child_dict and self.child_dict[(r.data,x1)]==self.child_dict[(r.data,x2)]:
            if self.child_dict[(r.data,x1)]==0:      #if x1 and x2 are both at the left subtree of r
                r=r.left
            else:       #else x1 and x2 are both at the right subtree of r
                r=r.right
        return r
    
    
    ''' In this function, we perform two tasks:
            First is to find if the node is in the tree
            Second is to maintain a dictionary to record the relationship of the target node and it's ancestors
            If the x is in the left subtree of r, then (r.data,x):0 else (r.data,x):1
            e.g. (5,12):0 means 12 is in 5's left subtree
    '''
    def is_find(self,r,x):
        if not r:
            return False
        if r.data==x:
            return True
        if self.is_find(r.left,x):
            self.child_dict[(r.data,x)]=0
            return True
        elif self.is_find(r.right, x):
            self.child_dict[(r.data,x)]=1
            return True
        else:
            return False
        
    def get_node_NR(self,r,x):
        stack=[]
        stack.append(r)
        while stack:    
            p=stack[-1]
            if p.data==x:
                return p
            stack.pop()
            if p.right!=None:
                stack.append(p.right)
            if p.left!=None:
                stack.append(p.left)
                
    def get_node(self,r,x):
        if not r:
            return None;
        if r.data==x:
            return r
        left_return=self.get_node(r.left,x)
        right_return=self.get_node(r.right,x)
        
        if left_return:
            return left_return
        elif right_return:
            return right_return
        else:
            return None
                
if __name__=='__main__':
    ''' The tree is:
                     1
                   /   \ 
                 2      3
                / \    / \
               4   5  8   9
                  / \    / \
                 6   7  10  11
                /
               12
    '''
    t=BinaryTree();
    pre_order=[1,2,4,5,6,12,7,3,8,9,10,11]
    in_order=[4,2,12,6,5,7,1,8,3,10,9,11]
    root=t.create_tree(pre_order, in_order)
    print 'Test pre_order_printNR'
    t.pre_order_printNR(root)
    print 'Test in_order_printNR'
    t.in_order_printNR(root)
    print 'Test level_order_print'
    t.level_order_print(root)
    print 'Tree height is', t.get_height(root)
    
    
    print t.is_find(root, 12)
    print t.child_dict
    x1=7
    x2=7
    print 'The lowest common ancestor of', x1, x2,'is:', t.get_loweset_ancestor(root, x1,x2).data

    print 'Testing get node'
    for node in pre_order:
        print t.get_node(root, node),