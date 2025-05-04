from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_safe, require_http_methods
from .models import Book, Thread, Comment, Category
from .forms import CommentForm, ThreadForm


# 쓰레드 댓글 생성
@login_required
@require_POST
def create_comment(request, book_pk, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk, book__pk=book_pk)
    
    # 폼 데이터가 유효한지 확인
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.thread = thread
        comment.user = request.user
        comment.save()

        # 댓글 목록을 반환 (AJAX 요청에 대한 응답으로 JSON 반환)
        comments = thread.comments.all()
        return JsonResponse({
            'content': comment.content,
            'username': comment.user.username,
            'comment_id': comment.pk,
            'comments': [
                {
                    'content': c.content,
                    'username': c.user.username,
                    'comment_id': c.pk,
                } for c in comments
            ]
        })
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)


# 쓰레드 댓글 삭제
@login_required
@require_POST
def delete_comment(request, book_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # 댓글을 작성한 사용자만 삭제 가능
    if comment.user == request.user:
        comment.delete()
        return JsonResponse({'success': True, 'comment_id': comment.pk})
    else:
        return JsonResponse({'error': '삭제 권한이 없습니다.'}, status=403)


# 전체 도서 목록을 반환하는 index 뷰
def index(request):
    books = Book.objects.all()
    # 카테고리 목록도 함께 전달해 필터링 할 수 있게
    categories = Category.objects.all()

    context = {
        'books': books,
        'categories': categories,
    }
    return render(request, 'books/index.html', context)


# 특정 도서의 상세 페이지를 반환하는 detail 뷰
@require_safe
def detail(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    form = CommentForm()
    
    context = {
        'book': book,
    }
    return render(request, 'books/detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def thread_create(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)

    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.book = book
            thread.user = request.user
            thread.save() 

            return redirect('books:thread_detail', book.pk, thread.pk)
    else:
        form = ThreadForm()

    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'books/thread_create.html', context)


@require_safe
def thread_detail(request, book_pk, thread_pk):
    book = get_object_or_404(Book, pk=book_pk)
    thread = get_object_or_404(Thread, pk=thread_pk, book=book)
    form = CommentForm()
    comments = Comment.objects.filter(thread=thread)

    context = {
        'book': book,
        'thread': thread,
        'comment_form': form,
        'comments': comments,
    }
    return render(request, 'books/thread_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def thread_update(request, book_pk, thread_pk):
    book = get_object_or_404(Book, pk=book_pk)
    thread = get_object_or_404(Thread, pk=thread_pk, book=book)

    # 쓰레드를 작성한 사용자만 수정할 수 있도록 확인
    if thread.user != request.user:
        return redirect('books:detail', book_pk=book.pk)

    if request.method == 'POST':
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()  
            return redirect('books:thread_detail', book.pk, thread.pk)
    else:
        form = ThreadForm(instance=thread)

    context = {
        'form': form,
        'book': book,
        'thread': thread,
    }
    return render(request, 'books/thread_update.html', context)


@login_required
@require_POST
def thread_delete(request, book_pk, thread_pk):
    book = get_object_or_404(Book, pk=book_pk)
    thread = get_object_or_404(Thread, pk=thread_pk, book=book)

    # 쓰레드를 작성한 사용자만 삭제할 수 있도록 확인
    if thread.user == request.user:
        thread.delete() 
        return redirect('books:detail', book.pk)  # 삭제 후 책 상세 페이지로 리디렉션
    else:
        return redirect('books:detail', book.pk)  # 삭제 권한이 없으면 책 상세 페이지로 리디렉션


def likes(request, book_pk, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk, book__pk=book_pk)

    # 사용자가 이미 좋아요를 눌렀는지 확인
    if request.user in thread.likes.all():
        # 이미 좋아요를 눌렀다면, 좋아요 취소
        thread.likes.remove(request.user)
        liked = False
    else:
        # 좋아요를 누르지 않았다면, 좋아요 추가
        thread.likes.add(request.user)
        liked = True

    # 좋아요 개수 갱신
    likes_count = thread.likes.count()

    # 좋아요 상태와 좋아요 개수를 반환
    return JsonResponse({'liked': liked, 'likes_count': likes_count})


def filter_category(request):
    selected_category = request.GET.get('category', None)
    category = Category.objects.get(name=selected_category)

    if selected_category:
        books = Book.objects.filter(category=category)
    else:
        # 카테고리가 선택되지 않으면 모든 도서 조회
        books = Book.objects.all()

    # 책 데이터 반환
    book_list = [{
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'book_id': book.pk,
        'cover': book.cover if book.cover else None,
    } for book in books]

    return JsonResponse({'books': book_list})
