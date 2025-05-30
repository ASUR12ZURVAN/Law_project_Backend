import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document_Text
from .serializers import DocumentSerializer
import re

# Configure your Gemini API key
genai.configure(api_key="AIzaSyDCwveXGSLTSju0oVAarSYiau0dtpAzvLQ")

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

class AnalyzeDocumentView(APIView):
    def post(self, request):
        text = request.data.get('Text', '')

        if not text:
            return Response({"error": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)

        clauses = re.split(r'(?i)clause \d+:', text)
        clauses = [c.strip() for c in clauses if c.strip()]
        total_clauses = len(clauses)

        # Prompt for Gemini
        prompt = f"""
You are a legal AI assistant giving format wise result. Analyze the following legal document and:
1. Identify and return number of total clauses.
2. Identify and return number of dangerous clauses.
3. List each dangerous clause in one line.
4. Provide 3 practical one-line suggestions to make the document safer.
5. Give a proofreading score (0–100).
while following the blueprint

   "id":string,
  "Text":shortened text of the input text(string),
  "Total_Clauses":number,
  "Dangerous_Clause":number,
  "Generated_Suggestions_Number":number,
  "ProofReading_Score":number,
  "Risk_Summary":string,
  "Dangerous_Clauses":string[]
  "Suggestions":string[],
  "Proofreading_Fixes":string[]

Legal Document:
{text}
"""

        try:
            response = model.generate_content(prompt)
            output_text = response.text

            # Extract values (basic parsing logic — improve with regex as needed)
            dangerous_clauses = len(re.findall(r'dangerous clause', output_text, re.IGNORECASE))
            suggestions_list = re.findall(r'Suggestion[s]?:\s*(.+)', output_text, re.IGNORECASE)
            proofreading_score_matches = re.findall(r'proofreading score.*?(\d{1,3})', output_text.lower())
            proofreading_score = int(proofreading_score_matches[0]) if proofreading_score_matches else 100

            # Save to DB
            document = Document_Text.objects.create(
                Text=text,
                Total_Clauses=total_clauses,
                Dangerous_Clauses=dangerous_clauses,
                suggestions_generated=output_text.strip(),
                suggestions=len(suggestions_list),
                Proofreading_score=proofreading_score
            )

            serializer = DocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": "Gemini API failed", "details": str(e)}, status=500)
        


class ListAnalyzedDocumentsView(APIView):
    def get(self, request):
        documents = Document_Text.objects.all().order_by('-id')  # latest first
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# GET a specific document by ID
class RetrieveAnalyzedDocumentView(APIView):
    def get(self, request, pk):
        try:
            document = Document_Text.objects.get(pk=pk)
            serializer = DocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Document_Text.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)