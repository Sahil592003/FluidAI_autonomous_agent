
"""Universal prompt templates for the FluidAI agent."""

UNIVERSAL_PLANNER_PROMPT = """
You are an expert document planner and strategist. Your task is to analyze ANY user request and create a comprehensive execution plan.

User Request: {request}

Your analysis must:
1. Identify the document type (any type - from business to technical to creative)
2. Extract key requirements and context
3. Make intelligent assumptions for missing information
4. Create 5-10 logical tasks for document creation
5. Adapt to any domain (business, technical, creative, academic, legal, etc.)

Return ONLY a JSON object with this EXACT structure:
{{
    "document_type": "Specific document type (e.g., Business Proposal, Technical Spec, Marketing Plan, Legal Contract, Research Paper, etc.)",
    "assumptions": [
        "Clear, reasonable assumption 1",
        "Clear, reasonable assumption 2",
        "Clear, reasonable assumption 3"
    ],
    "tasks": [
        "Task 1: Create executive summary/overview",
        "Task 2: Write introduction and context",
        "Task 3: Define objectives and scope",
        "Task 4: Describe core solution or approach",
        "Task 5: Provide implementation details or methodology",
        "Task 6: Outline timeline and resources",
        "Task 7: Identify risks and mitigation strategies",
        "Task 8: Write conclusion and next steps"
    ]
}}

Guidelines:
- Tasks must be specific, actionable, and in logical order
- Adapt section names based on document type (e.g., "Methodology" for research, "Technical Architecture" for software, "Marketing Channels" for marketing)
- Create 5-10 tasks depending on document complexity
- Make assumptions that are reasonable and clearly stated
- Return ONLY valid JSON, no other text
"""


UNIVERSAL_EXECUTOR_PROMPT = """
You are an expert content writer specializing in ALL document types. Write a professional, comprehensive section for a document.

Document Type: {document_type}
Section Name: {section_name}
Context: {context}

Previous Content (for continuity):
{previous_content}

Write a detailed, professional section that:
- Is perfectly tailored to the document type and section
- Uses appropriate industry terminology and tone
- Is specific, actionable, and informative
- Includes relevant details, examples, and data where appropriate
- Is 200-400 words for most sections
- Maintains consistency with previous sections
- Is immediately usable in a professional setting

The writing style should match the document type:
- Business: Formal, strategic, results-oriented
- Technical: Precise, clear, detailed
- Creative: Engaging, descriptive, compelling
- Academic: Scholarly, referenced, objective
- Legal: Precise, formal, unambiguous
- Marketing: Persuasive, benefit-focused, energetic

Return ONLY the section content with proper formatting (paragraphs, bullet points if needed).
"""


UNIVERSAL_REFLECTION_PROMPT = """
You are a senior document reviewer and quality assurance expert. Review this document thoroughly.

Document Type: {document_type}
Original Request: {original_request}
Assumptions Made: {assumptions}

Document Content:
{document_content}

Perform a comprehensive review covering:

1. COMPLETENESS:
   - Is the document complete for its type?
   - Are all required sections present?
   - Are there any obvious gaps?

2. STRUCTURE:
   - Is the logical flow appropriate?
   - Is the information properly organized?
   - Are transitions smooth?

3. PROFESSIONALISM:
   - Is the tone appropriate for the document type?
   - Is the language clear and professional?
   - Is the formatting appropriate?

4. QUALITY:
   - Is the content specific and actionable?
   - Are there enough details and examples?
   - Is the reasoning sound?

5. ASSUMPTIONS:
   - Are the assumptions reasonable?
   - Are they clearly stated?
   - Should any be added or modified?

Return a JSON object with this structure:
{{
    "is_complete": boolean,
    "completeness_score": 0-10,
    "structure_score": 0-10,
    "professionalism_score": 0-10,
    "quality_score": 0-10,
    "overall_score": 0-10,
    "missing_elements": ["Specific missing elements"],
    "structure_issues": ["Specific structure issues"],
    "quality_issues": ["Specific quality issues"],
    "improvements": ["Specific, actionable improvements"],
    "assumptions_feedback": "Feedback on assumptions",
    "final_verdict": "ready" or "needs_improvement" or "needs_major_revision"
}}
"""


UNIVERSAL_SUMMARIZER_PROMPT = """
Create a concise, professional executive summary for this document.

Document Type: {document_type}
Document Content:
{document_content}

The summary should:
- Be 2-3 sentences
- Capture the purpose and key points
- Highlight the most important outcomes or recommendations
- Be compelling and action-oriented
- Match the tone of the document type

Return ONLY the summary paragraph, no other text.
"""


UNIVERSAL_SECTION_TEMPLATES = {
    "Business Proposal": [
        "Executive Summary",
        "Business Case",
        "Market Analysis",
        "Solution Overview",
        "Implementation Plan",
        "Financial Projections",
        "Risk Assessment",
        "Success Metrics",
        "Conclusion"
    ],
    "Technical Document": [
        "Executive Summary",
        "Introduction",
        "System Architecture",
        "Technical Specifications",
        "Implementation Details",
        "Testing Strategy",
        "Deployment Plan",
        "Security Considerations",
        "Maintenance",
        "Conclusion"
    ],
    "Project Plan": [
        "Executive Summary",
        "Project Overview",
        "Objectives",
        "Scope",
        "Methodology",
        "Timeline",
        "Resources",
        "Budget",
        "Risk Management",
        "Stakeholder Communication",
        "Success Criteria"
    ],
    "Marketing Plan": [
        "Executive Summary",
        "Market Research",
        "Target Audience",
        "Competitive Analysis",
        "Marketing Strategy",
        "Marketing Channels",
        "Content Strategy",
        "Budget",
        "KPIs",
        "Timeline",
        "Conclusion"
    ],
    "Research Paper": [
        "Abstract",
        "Introduction",
        "Literature Review",
        "Methodology",
        "Results",
        "Discussion",
        "Conclusion",
        "References",
        "Appendices"
    ],
    "Legal Document": [
        "Preamble",
        "Definitions",
        "Scope",
        "Terms and Conditions",
        "Obligations",
        "Rights",
        "Termination",
        "Liability",
        "Indemnification",
        "Governing Law",
        "Signatures"
    ],
    "Software Requirements": [
        "Executive Summary",
        "Project Overview",
        "Functional Requirements",
        "Non-Functional Requirements",
        "User Interface",
        "System Architecture",
        "Data Requirements",
        "Security Requirements",
        "Performance Requirements",
        "Constraints",
        "Assumptions"
    ],
    "Training Manual": [
        "Introduction",
        "Learning Objectives",
        "Getting Started",
        "Step-by-Step Procedures",
        "Best Practices",
        "Troubleshooting",
        "Tips and Tricks",
        "Assessment",
        "Resources",
        "Conclusion"
    ],
    "Healthcare Proposal": [
        "Executive Summary",
        "Healthcare Need",
        "Solution Overview",
        "Clinical Approach",
        "Technology Stack",
        "Compliance Framework",
        "Implementation Timeline",
        "Resource Requirements",
        "Budget Estimate",
        "Risk Assessment",
        "Success Metrics",
        "Conclusion"
    ],
    "Default": [
        "Executive Summary",
        "Introduction",
        "Objectives",
        "Scope",
        "Solution Overview",
        "Architecture",
        "Timeline",
        "Risks",
        "Conclusion"
    ]
}