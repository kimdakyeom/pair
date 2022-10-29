from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, Comment
from .forms import CommentForm, ReviewForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def index(request):
    review = Review.objects.all().order_by("-pk")
    context = {"review": review}
    return render(request, "reviews/index.html", context)


def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()

    context = {
        "review": review,
        "comment_form": comment_form,
    }
    return render(request, "reviews/detail.html", context)


def comments(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        context = {
            "content": comment.content,
            "userName": comment.user.username,
        }
    return JsonResponse(context)


@login_required
def create(request):
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            db_review_form = review_form.save(commit=False)
            db_review_form.user = request.user
            db_review_form.save()
            return redirect("reviews:index")
    else:
        review_form = ReviewForm()
    return render(request, "reviews/create.html", {"review_form": review_form})


def update(request, pk):
    db_review_form = Review.objects.get(pk=pk)

    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=db_review_form)

        if review_form.is_valid():
            review_form.save()

            return redirect("reviews:index")

    else:
        review_form = ReviewForm(instance=db_review_form)

    return render(request, "reviews/create.html", {"review_form": review_form})


def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()

    return redirect("reviews:index")


@login_required
def like(request, pk):
    review = Review.objects.get(pk=pk)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if article.like_users.filter(id=request.user.id).exists():
    if request.user in review.like_users.all():
        # 좋아요 삭제하고
        review.like_users.remove(request.user)
    else:
        # 좋아요 추가하고
        review.like_users.add(request.user)
    # 상세 페이지로 redirect
    return redirect("reviews:detail", pk)


def category(request, val):
    if val == "1":
        reviews = Review.objects.all().order_by("-pk")
    elif val == "2":
        reviews = Review.objects.filter(category=val)
    elif val == "3":
        reviews = Review.objects.filter(category=val)
    relist = []
    for r in reviews:
        user = get_user_model().objects.get(pk=r.user_id)
        relist.append(
            {
                "user": user.username,
                "pk": r.pk,
                "title": r.title,
                "content": r.content,
                "movie_name": r.movie_name,
                "grade": r.grade,
                "created_at": r.created_at,
                "updated_at": r.updated_at,
                "category": r.category,
            }
        )
    context = {
        "relist": relist,
    }
    return JsonResponse(context)
