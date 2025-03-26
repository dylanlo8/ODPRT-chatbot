from deepeval import evaluate
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams, LLMTestCase
from deepeval.dataset import EvaluationDataset

from chatbot.backend.evaluation.params import AGREEMENT_TYPE_QUERIES, AGREEMENT_TYPE_GROUND_TRUTH, GENERAL_QUERIES, GENERAL_GROUND_TRUTH, IEP_CONRACTING_HUB_QUERIES, IEP_CONTRACTING_HUB_GROUND_TRUTH, REDIRECT_TTI_QUERIES, REDIRECT_TTI_GROUND_TRUTH, REDIRECT_OLA_QUERIES, REDIRECT_OLA_GROUND_TRUTH, REDIRECT_IRB_QUERIES, REDIRECT_IRB_GROUND_TRUTH, PRE_AWARD_QUERIES, PRE_AWARD_GROUND_TRUTH, POST_AWARD_QUERIES, POST_AWARD_GROUND_TRUTH
from chatbot.backend.inference.response_generator import ResponseGenerator
from chatbot.backend.services.vector_db.db import vector_db
from chatbot.backend.services.logger import logger



class Evaluator:
    def __init__(
        self,
    ):
        self.response_generator = ResponseGenerator()
        self.vector_db = vector_db
        self.logger = logger

    def _get_metrics(self):
        correctness_metric = GEval(
            name="Correctness",
            criteria="Determine whether the actual output is factually correct based on the expected output.",
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT,
            ],
            threshold=0.7
        )

        contextual_precision_metric = GEval(
            name="Contextual Precision",
            criteria="Assess the precision of the actual output concerning the provided context.",
            evaluation_params=[
                LLMTestCaseParams.CONTEXT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ]
        )

        contextual_recall_metric = GEval(
            name="Contextual Recall",
            criteria="Determine how well the actual output recalls information from the provided context.",
            evaluation_params=[
                LLMTestCaseParams.CONTEXT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ]
        )

        faithfulness_metric = GEval(
            name="Faithfulness",
            criteria="Check the factual accuracy of the actual output based on the provided context.",
            evaluation_params=[
                LLMTestCaseParams.CONTEXT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ]
        )
        return {
            "correctness": correctness_metric,
            "contextual_precision": contextual_precision_metric,
            "contextual_recall": contextual_recall_metric,
            "faithfulness": faithfulness_metric,
        }

    def _get_test_cases(self, query, truth):
        test_cases = []
        self.logger.info("[ResponseGenerator] generating responses")
        for q, ground_truth in zip(query, truth):
            _, context_list = self.vector_db.hybrid_search(query=q)
            response = self.response_generator._generate_answer(user_query=q)
            test_case = LLMTestCase(
                input=q,
                actual_output=response,
                expected_output=ground_truth,
                context=context_list,
            )
            test_cases.append(test_case)
        return test_cases

    def build_metrics_and_dataset(self, query, truth):
        test_cases = self._get_test_cases(query, truth)
        self.logger.info("[Evaluator] building the dataset")
        dataset = EvaluationDataset(test_cases=test_cases)
        metrics = self._get_metrics()
        return metrics, dataset

    def run_evaluation(self, query, truth):
        metrics, dataset = self.build_metrics_and_dataset(query, truth)
        self.logger.info(f"[Evaluator] evaluating the dataset")
        evaluate(dataset, [metric for metric in metrics.values()])


if __name__ == "__main__":
    types = ["AGREEMENT_TYPE", "GENERAL", "IEP_CONTRACTING_HUB", "REDIRECT_TTI", "REDIRECT_OLA", "REDIRECT_IRB", "PRE_AWARD", "POST_AWARD"]
    queries = [AGREEMENT_TYPE_QUERIES, GENERAL_QUERIES, IEP_CONRACTING_HUB_QUERIES, REDIRECT_TTI_QUERIES, REDIRECT_OLA_QUERIES, REDIRECT_IRB_QUERIES, PRE_AWARD_QUERIES, POST_AWARD_QUERIES]
    ground_truth = [AGREEMENT_TYPE_GROUND_TRUTH, GENERAL_GROUND_TRUTH, IEP_CONTRACTING_HUB_GROUND_TRUTH, REDIRECT_TTI_GROUND_TRUTH, REDIRECT_OLA_GROUND_TRUTH, REDIRECT_IRB_GROUND_TRUTH, PRE_AWARD_GROUND_TRUTH, POST_AWARD_GROUND_TRUTH]
    for i in range(len(queries)):
        evaluator = Evaluator()
        evaluator.logger.info(f"[Evaluator] running evaluation for {types[i]}")
        evaluator.run_evaluation(queries[i], ground_truth[i])
