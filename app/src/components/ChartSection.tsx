import React from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

const ChartSection = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <section id="analysis" className="py-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 50 }}
          animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4 font-serif tracking-tight">Analysis</h2>
          <div className="prose prose-lg max-w-4xl mx-auto">
            <p className="text-xl text-gray-700 mb-8 font-sans leading-relaxed">
              The analysis of France's HPAI vaccination campaign employs an interrupted time series approach to evaluate the intervention's effectiveness against the backdrop of broader European outbreak patterns. This analytical framework provides a robust method for assessing the campaign's impact while accounting for regional trends and seasonal variations in outbreak occurrence.
            </p>
            
            <p className="text-lg text-gray-600 mb-10 font-sans leading-relaxed">
              This analysis spans from November 2021 to January 2025, encompassing three distinct periods: pre-vaccination (November 2021 - September 2023), vaccination implementation (October 2023 - October 2024), and early post-vaccination (November 2024 - January 2025). This temporal division allows for the examination of both immediate and potential lasting effects of the vaccination program.
            </p>

            <div className="bg-gray-50 p-8 rounded-lg mb-10 shadow-sm">
              <h3 className="text-2xl font-serif font-bold mb-6 text-gray-900">Statistical Framework</h3>
              <p className="mb-6 font-sans leading-relaxed">The primary analysis utilizes a segmented regression model that accommodates both level and slope changes:</p>
              <div className="bg-white p-6 rounded-lg font-mono text-sm mb-6 shadow-sm">
                Yt = β0 + β1T + β2Xt + β3TXt + β4Zt + εt
              </div>
              <p className="font-sans mb-4">Where:</p>
              <ul className="list-disc list-inside space-y-2 font-sans">
                <li className="text-gray-700">Yt represents monthly outbreak counts</li>
                <li className="text-gray-700">T denotes time as a continuous variable</li>
                <li className="text-gray-700">Xt is the intervention indicator (0 pre-vaccination, 1 post-vaccination)</li>
                <li className="text-gray-700">TXt captures the slope change following intervention</li>
                <li className="text-gray-700">Zt represents seasonal adjustment factors</li>
                <li className="text-gray-700">εt is the error term, assumed to follow normal distribution</li>
              </ul>
            </div>

            <div className="bg-gray-50 p-8 rounded-lg mb-10 shadow-sm">
              <h3 className="text-2xl font-serif font-bold mb-6 text-gray-900">Model Estimation Strategy</h3>
              <p className="mb-6 font-sans leading-relaxed">
                We employ ordinary least squares (OLS) estimation with robust standard errors to account for potential heteroskedasticity in outbreak counts. The model's parameters provide specific insights:
              </p>
              <ul className="list-disc list-inside space-y-2 font-sans">
                <li className="text-gray-700">β0 estimates the baseline level</li>
                <li className="text-gray-700">β1 captures the underlying temporal trend</li>
                <li className="text-gray-700">β2 quantifies the immediate intervention effect</li>
                <li className="text-gray-700">β3 identifies changes in the outbreak trajectory post-intervention</li>
                <li className="text-gray-700">β4 controls for seasonal variation</li>
              </ul>
            </div>

            <div className="bg-gray-50 p-8 rounded-lg mb-10 shadow-sm">
              <h3 className="text-2xl font-serif font-bold mb-6 text-gray-900">Counterfactual Construction</h3>
              <p className="mb-6 font-sans leading-relaxed">To strengthen causal inference, we implement a difference-in-differences (DiD) framework:</p>
              <div className="bg-white p-6 rounded-lg font-mono text-sm mb-6 shadow-sm">
                DiD = (YF,post - YF,pre) - (YC,post - YC,pre)
              </div>
              <p className="font-sans mb-4">Where:</p>
              <ul className="list-disc list-inside space-y-2 font-sans">
                <li className="text-gray-700">YF,post represents French outbreaks post-intervention</li>
                <li className="text-gray-700">YF,pre represents French outbreaks pre-intervention</li>
                <li className="text-gray-700">YC,post represents control group outbreaks post-intervention</li>
                <li className="text-gray-700">YC,pre represents control group outbreaks pre-intervention</li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default ChartSection;