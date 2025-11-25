
class TreeNode:
    def __init__(self, aabb, obj=None):
        self.aabb = aabb     # AABBBox
        self.obj = obj       # 실제 GameObject
        self.parent = None
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None


class AABBTree:
    def __init__(self):
        self.root = None

    # AABB와 다른 AABB의 합집합 생성
    def merge_aabb(self, aabb1, aabb2):
        return aabb1.merge(aabb2)

    # 삽입
    def insert(self, obj, aabb):
        new_node = TreeNode(aabb, obj)

        # 트리가 비었으면 루트로 삽입
        if self.root is None:
            self.root = new_node
            return new_node

        # 1. 삽입할 위치 찾기 (Leaf까지 내려감)
        leaf = self.choose_best_leaf(self.root, new_node.aabb)

        # 2. 새로운 부모 노드 생성
        old_parent = leaf.parent
        new_parent_aabb = self.merge_aabb(leaf.aabb, new_node.aabb)
        new_parent = TreeNode(new_parent_aabb)

        new_parent.parent = old_parent
        new_parent.left = leaf
        new_parent.right = new_node

        leaf.parent = new_parent
        new_node.parent = new_parent

        if old_parent is None:
            self.root = new_parent
        else:
            # 기존 부모가 leaf를 자식으로 갖고 있었으니 교체
            if old_parent.left is leaf:
                old_parent.left = new_parent
            else:
                old_parent.right = new_parent

            # 부모의 AABB는 틀어졌으므로 위로 올라가며 업데이트
            self.update_aabb_upwards(old_parent)

        return new_node

    # AABB 갱신 (물체 이동 시 호출)
    def update(self, node, new_aabb):
        if node is None:
            return

        # AABB 변화가 없다면 패스
        if (node.aabb.minx == new_aabb.minx and
            node.aabb.miny == new_aabb.miny and
            node.aabb.maxx == new_aabb.maxx and
            node.aabb.maxy == new_aabb.maxy):
            return node

        # 트리에서 제거 후 다시 삽입
        self.remove(node)
        return self.insert(node.obj, new_aabb)

    # 제거
    def remove(self, node):
        if node == self.root:
            self.root = None
            return

        parent = node.parent
        grand = parent.parent
        sibling = parent.left if parent.right is node else parent.right

        if grand is None:
            self.root = sibling
            sibling.parent = None
        else:
            if grand.left is parent:
                grand.left = sibling
            else:
                grand.right = sibling
            sibling.parent = grand
            self.update_aabb_upwards(grand)

    #  충돌 후보 반환 (Query)
    def query(self, aabb):
        """주어진 AABBBox와 충돌 가능성이 있는 leaf들의 obj 리스트 반환"""
        result = []
        stack = [self.root]

        while stack:
            node = stack.pop()
            if node is None:
                continue

            if not node.aabb.intersects(aabb):
                continue  # 충돌 가능성 없음 → 패스

            if node.is_leaf():
                result.append(node.obj)
            else:
                stack.append(node.left)
                stack.append(node.right)

        return result

    # 삽입할 Leaf 결정 (Surface Area Heuristic)
    def choose_best_leaf(self, node, aabb):
        if node.is_leaf():
            return node

        # 자식을 합쳤을 때 면적 증가량 계산
        left = node.left
        right = node.right

        area_left = left.aabb.merge(aabb).area()
        area_right = right.aabb.merge(aabb).area()

        # 면적 증가량이 작은 쪽으로 내려감
        if area_left < area_right:
            return self.choose_best_leaf(left, aabb)
        else:
            return self.choose_best_leaf(right, aabb)

    # AABB 부모 방향으로 갱신
    def update_aabb_upwards(self, node):
        while node is not None:
            if not node.is_leaf():
                node.aabb = node.left.aabb.merge(node.right.aabb)
            node = node.parent


    # 디버그용: 트리 출력
    def draw_tree(self, screen):
        #if self.root is None:
        #    return
        self._draw_node(screen, self.root)

    def _draw_node(self, screen, node):
        if node is None:
            return

        import pygame

        # AABB 정보
        x = node.aabb.minx
        y = node.aabb.miny
        w = node.aabb.maxx - node.aabb.minx
        h = node.aabb.maxy - node.aabb.miny

        # 리프 = 초록색 / 내부노드 = 빨간색
        color = (0, 255, 0) if node.is_leaf() else (0, 255, 255)

        # 얇은 선으로 박스 그리기
        pygame.draw.rect(screen, color, pygame.Rect(x, y, w, h), 1)

        # 자식 노드 재귀 호출
        if not node.is_leaf():
            self._draw_node(screen, node.left)
            self._draw_node(screen, node.right)