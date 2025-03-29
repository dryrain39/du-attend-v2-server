# FontAwesome에서 Lucide Icons로의 마이그레이션

## 문제 상황

프로젝트에서 FontAwesome을 사용하고 있었으나, 이를 더 가볍고 모던한 Lucide Icons로 교체할 필요가 있었습니다.

## 주요 변경 사항

### 1. Lucide Icons 초기화 설정

`header.html` 파일에 Lucide Icons 초기화 코드를 추가했습니다:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    lucide.createIcons({
        attrs: {
            'stroke-width': 1.5,
            'vertical-align': '-0.125em' // 수직 정렬 조정
        }
    });
});
```

### 2. CSS 스타일 추가

아이콘 정렬 및 크기 조정을 위한 CSS 스타일을 추가했습니다:

```css
[data-lucide] {
    vertical-align: text-bottom;
}

.copyleft [data-lucide] {
    width: 14px;
    height: 14px;
}
```

### 3. FontAwesome에서 Lucide로 아이콘 교체

다음과 같은 아이콘들을 교체했습니다:

- `fa-solid fa-times` → `data-lucide="x"`
- `fa-solid fa-magnifying-glass` → `data-lucide="search"`
- `fa-solid fa-plus` → `data-lucide="plus"`
- `fa-solid fa-qrcode` → `data-lucide="qr-code"`
- `fa-solid fa-gear` → `data-lucide="settings"`
- `fa-solid fa-bullhorn` → `data-lucide="megaphone"`
- `fa-regular fa-circle-question` → `data-lucide="help-circle"`
- `fa-solid fa-people-group` → `data-lucide="users"`
- `fa-solid fa-arrow-right` → `data-lucide="arrow-right"`
- `fa-solid fa-arrow-up-right-from-square` → `data-lucide="external-link"`
- `fa-solid fa-pen-to-square` → `data-lucide="edit"`
- `fa-solid fa-trash` → `data-lucide="trash-2"`
- `fa-solid fa-arrow-left` → `data-lucide="arrow-left"`
- `fa-solid fa-heart` → `data-lucide="heart"`
- `fa-solid fa-house` → `data-lucide="home"`

### 4. 공지사항 모달 기능 추가

배너에서 짧은 공지를 클릭하면 모달이 표시되도록 기능을 추가했습니다:

1. `index.html`에 Bootstrap 모달 컴포넌트 추가
2. `showNotice()` 함수 구현
3. 배너에 클릭 이벤트 추가

```html
<div class="modal fade" id="noticeModal" tabindex="-1" aria-labelledby="noticeModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="noticeModalLabel">공지사항</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body" id="noticeModalBody">
        <!-- 모달 내용이 여기에 표시됩니다 -->
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
      </div>
    </div>
  </div>
</div>
```

```javascript
function showNotice(title, message) {
    document.getElementById('noticeModalLabel').textContent = title;
    document.getElementById('noticeModalBody').innerHTML = message;
    var noticeModal = new bootstrap.Modal(document.getElementById('noticeModal'));
    noticeModal.show();
}
```

## 개선 효과

1. **더 가벼운 로딩 속도**: Lucide Icons는 FontAwesome보다 더 가볍습니다.
2. **모던한 디자인**: SVG 기반 아이콘으로 더 현대적인 디자인을 제공합니다.
3. **더 나은 접근성**: 필요에 따라 아이콘 크기와 색상을 쉽게 조정할 수 있습니다.
4. **사용자 경험 개선**: 공지사항을 모달로 표시하여 정보 접근성이 향상되었습니다.

## 남은 과제

- FontAwesome 스크립트는 다른 페이지에서 사용될 수 있으므로 완전히 제거하지 않고 주석 처리했습니다.
- 필요에 따라 더 많은 아이콘들을 Lucide로 교체할 수 있습니다.
- 강의실 수정 페이지에서 강의실 순서 변경 기능 추가가 요청되었습니다.
