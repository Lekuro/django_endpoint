from django.http import JsonResponse
from itertools import permutations
from nltk.tree import ParentedTree
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ParaphraseSerializer
from rest_framework import status
from nltk.tree import *
import itertools


class ParaphraseView(APIView):
    def get(self, request):
        serializer = ParaphraseSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            tree = data['tree']
            limit = data.get('limit', 20)
            print('tree', tree)
            print('limit', limit)
            # Parse the input tree
            parsed_tree = ParentedTree.fromstring(tree)
            results = []
            for subtree in parsed_tree.subtrees(lambda t: t.label() == "NP" and len(t) > 1):
                # Create a list of tuples representing the possible permutations of the subtrees' children
                permutations = list(
                    itertools.permutations(subtree, len(subtree)))
                # Limit the number of permutations
                permutations = permutations[:limit]
                # Create a list of trees representing each permutation
                trees = [ParentedTree(subtree.label(), list(perm)) if isinstance(perm[0], str) else ParentedTree(
                    subtree.label(), [ParentedTree(child.label(), child.leaves()) for child in perm]) for perm in permutations]
                # Serialize each tree as a string and add to the results
                # results.extend([tree.pformat() for tree in trees])
                results.extend([{'tree': tree.pformat()}
                                for tree in trees])
            # Return the response as JSON
            response = {'paraphrases':  results}
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
