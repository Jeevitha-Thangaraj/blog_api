from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Q

# Create Post
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response({"message": "Post created", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve Post
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

# Update Post
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if post.author != request.user:
            return Response({"message": "You are not the author of this post."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Post updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

# Delete Post
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if post.author != request.user:
            return Response({"message": "You are not the author of this post."}, status=status.HTTP_403_FORBIDDEN)
        
        post.delete()
        return Response({"message": "Post deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request, post_id):
   try:
      post = Post.objects.get(pk=post_id)
      serializer = CommentSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save(post=post, author=request.user)
        return Response({"message": "Comment created", "data": serializer.data}, status=status.HTTP_201_CREATED)
   except:
    return Response({"message":"Comment not found"},serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def read_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response({"message": "Comment retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": "Error retrieving comment", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": "Error retrieving comment", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if comment.author != request.user:
        return Response({"message": "You are not authorized to update this comment."}, status=status.HTTP_403_FORBIDDEN)

    serializer = CommentSerializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save() 
        return Response({"message": "Comment updated", "data": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({"message": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": "Error retrieving comment", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if comment.author != request.user:
        return Response({"message": "You are not authorized to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_comments(request):
    try:
        comments = Comment.objects.all()

        search_query = request.query_params.get("search", None)
        if search_query:
            comments = comments.filter(Q(text__icontains=search_query))

        post_id = request.query_params.get("post", None)
        if post_id:
            comments = comments.filter(post__id=post_id)

        serializer = CommentSerializer(comments, many=True)
        return Response({"message": "Comments retrieved", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "Error retrieving comments", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





