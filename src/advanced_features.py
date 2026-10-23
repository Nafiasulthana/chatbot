class ResumeAnalyzer:
    """
    Controller class to manage different analysis modes for the resume screening system.
    Follows constraints: uses existing QA chain as a wrapper, separates core logic,
    and allows independent enablement of new features.
    """
    def __init__(self, qa_chain_func):
        self.qa_chain = qa_chain_func

    def process(self, mode: str, **kwargs):
        """Routing mechanism for feature selection."""
        if mode == "qa":
            return self.qa_chain({"input": kwargs.get("query")})["result"]
        elif mode == "job_fit":
            return self._calculate_job_fit(kwargs.get("job_description", ""))
        elif mode == "extract_profile":
            return self._extract_profile()
        elif mode == "portfolio_ui":
            return self._generate_portfolio_ui()
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def _calculate_job_fit(self, job_description: str):
        prompt = (
            f"Evaluate the candidate's fit for the following job description.\n\n"
            f"Job Description:\n{job_description}\n\n"
            f"Please provide a Job Fit Score (out of 100) and a short justification."
        )
        response = self.qa_chain({"input": prompt})
        return response["result"]

    def _extract_profile(self):
        prompt = (
            "Extract the following structured information about the candidate: "
            "1. Key Skills (list) "
            "2. Total Years of Experience "
            "3. Highest Education Level. "
            "Format the output clearly with headers."
        )
        response = self.qa_chain({"input": prompt})
        return response["result"]

    def _generate_portfolio_ui(self):
        prompt = (
            "You are an AI UI content generator integrated into a resume-based application. "
            "Your task is to dynamically replace the textual content of a predefined portfolio UI template. "
            "Do NOT change UI layout, hierarchy, or component structure. "
            "Only replace textual content and relevant labels. "
            "Maintain the same tone, spacing, and length as the original UI text. "
            "Ensure all content is professional, concise, and visually balanced. "
            "Preserve section intent (e.g., 'About Me', 'Projects', etc.). "
            "Output FORMAT: Return ONLY a structured JSON mapped EXACTLY to UI sections (Hero, QuickInfo, AboutMe, CodeSnippet, Skills, Projects, Experience, Education, Certifications, Extra). No explanation."
        )
        response = self.qa_chain({"input": prompt})
        return response["result"]
