from AABBTree import AABBTree

class BroadPhaseManager:
    def __init__(self):
        self.tree = AABBTree()
        self.nodes = {}  # obj → treeNode

    def add(self, obj):
        aabb = obj.collider.aabb_box()
        node = self.tree.insert(obj, aabb)
        self.nodes[obj] = node

    def remove(self, obj):
        if obj in self.nodes:
            node = self.nodes[obj]
            self.tree.remove(node)
            del self.nodes[obj]

    def update(self, obj):
        """오브젝트 이동 후 호출"""
        if obj not in self.nodes:
            return

        new_box = obj.collider.aabb_box()
        node = self.nodes[obj]
        new_node = self.tree.update(node, new_box)

        # update()가 새로운 노드 반환하는 경우 갱신
        if new_node is not None:
            self.nodes[obj] = new_node

    def query(self, obj):
        """자기 자신 제외한 충돌 후보 반환"""
        aabb = obj.collider.aabb_box()
        result = self.tree.query(aabb)
        return [x for x in result if x is not obj]
