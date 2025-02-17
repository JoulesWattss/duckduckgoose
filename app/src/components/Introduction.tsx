import React from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

const Introduction = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <section id="introduction" className="py-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 50 }}
          animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Introduction</h2>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="bg-white rounded-xl shadow-lg p-8 prose prose-lg max-w-none"
        >
          <p className="mb-6">
            In October 2023, France initiated Europe's first nationwide vaccination campaign against the H5N1 strain of highly pathogenic avian influenza (HPAI) in domestic poultry. This pioneering initiative targeted over 50 million domestic ducks raised for food production, representing a significant shift in European HPAI control strategies (Bourouiba et al., 2024; Nature Microbiology).
          </p>

          <p className="mb-6">
            HPAI H5N1, first identified in domestic geese in China in 1996, has evolved into a significant global health concern (Webster et al., 2022; The Lancet Infectious Diseases). The virus demonstrates particularly high pathogenicity in domestic poultry, with mortality rates frequently exceeding 90% in infected flocks (World Organisation for Animal Health [WOAH], 2023). Beyond its immediate impact on animal welfare, HPAI outbreaks severely disrupt poultry production and international trade, with global economic losses estimated at $35.8 billion between 2003 and 2021 (Food and Agriculture Organization [FAO], 2023).
          </p>

          <p className="mb-6">
            France's decision to implement vaccination emerged from a context of devastating seasonal outbreaks. Between 2020 and 2023, the country experienced increasingly severe HPAI waves, with peak outbreaks in winter 2022-2023 leading to the culling of approximately 20 million birds (Métras et al., 2024; Veterinary Research). Preliminary research conducted by the Veterinary School of Toulouse demonstrated a 98% reduction in infection rates within vaccinated populations under controlled conditions (Laurent et al., 2024; Vaccine).
          </p>

          <p className="mb-6">
            However, this innovative approach carries significant economic implications. Several countries, including the United States and United Kingdom, have imposed restrictions on French poultry products, citing concerns about potential virus circulation in vaccinated populations (European Food Safety Authority [EFSA], 2024). These trade restrictions highlight the complex balance between disease control and economic considerations in agricultural health policy. As a result, the extent and significance of the campaign results are highly important to consider when making these tradeoffs.
          </p>

          <p className="mb-6">
            The significance of France's vaccination campaign extends beyond national borders. As the first large-scale implementation of HPAI vaccination in Europe, its outcomes could influence future disease control policies globally (World Health Organization [WHO], 2024). While other countries have implemented limited vaccination programs—such as Finland's targeted vaccination of high-risk farmworkers—France's comprehensive approach to poultry vaccination remains unique in the European context (European Centre for Disease Prevention and Control [ECDC], 2024).
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default Introduction;