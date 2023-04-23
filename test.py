class A():
    def Hi(self):
        print("A")

class B(A):
    def Hi(self):
        super().Hi()
        print("B")

class C(B):
    def Hi(self):
        super().Hi()
        print("C")

a = C()
a.Hi()