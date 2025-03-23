QUERIES = [
    """I would like to transfer data from my collaborator for my research project, what agreement do I need?""",
    """What is the process for signing research agreements negotiated by IEP?""",
    """What is the difference between in-kind and cash contributions for partnerships?""",
    """Can we get the Research Collaboration Agreement (RCA) process started before the grant is awarded?""",
    """What is the Indirect Research Costs (IRC) for my research project?""",
    """Who do I contact for advice regarding purchase or procurement services (research or otherwise) / goods / equipment or leasing for equipment for research?""",
    """Where can I find grant or funding available in NUS?""",
    """I got a grant. What do I do next?""",
    """Can I apply for multiple WBS accounts for one grant? How do I apply for multiple WBS account?""",
    """Who do I submit my progress report to?""",
    """How do I ask for advance payment waiver for research related partnerships?""",
]

GROUND_TRUTH = [
    """For incoming data transfer (e.g. NUS is receiving data from collaborator), please contact Office of Legal Affairs (OLA) at olasec@nus.edu.sg.""",
    """Upon finalization of research agreement and prior to signing, the assigned IEP case officer will seek NUS management approval in accordance with NUS Policy of Approving and Signing Authority (NUS PASA).""",
    """In-kind contributions - Existing resources, which may also include external grant awarded to NUS for the research project but not transferred to collaborator.
        Cash contributions - Cash funding to be provided to the research project or received from collaborator.
        """,
    """It is preferred for the RCA to be put in place after the grant is awarded. 

        Please consider whether the RCA is still required if the grant is not awarded. If no, we would suggest waiting for the grant outcome. 

        If you have received an in-principal approval of the grant, you may submit your request to IEP Contracting Hub. If you do not have access to IEP Contracting Hub, please contact IEP-Admin for a user account to be created.
        """,
    """Please refer to NUS IRC Policy for more information on applicable IRC rates for your research project""",
    """Please contact Central Procurement Office (CPO) at askcpo@nus.edu.sg 

        You may find more details @https://proctor.nus.edu.sg/policy/
        """,
    """The Office of the Deputy President (Research & Technology) issues a monthly newsletter that lists funding opportunities available to NUS researchers.

Researchers may visit NUS' grant call portal, InfoReady, to view details of open grant calls.

NUS also offers internal programmes such as Humanities and Social Science Fellowships and Start-Up Grants to help new staff kick-off and build their research base at NUS.

Since many grantors strongly discourage researchers from submitting a single proposal to multiple funding agencies for funding consideration, PIs should make a calculated decision before sending in their applications.

For help, please contact the officer in charge of the programme.
""",
    """Research funding awarded to NUS staff and hosted by NUS may be conveyed:
•	Through online portals and grant management systems (e.g. NRF's IGMS, A*STAR's iGrants, NIE ROMS, etc.)
•	Via email in softcopy - Letter of Awards, Funding Agreements
The Grant Award Letter or Funding Agreement details the Host Institution and PI/Co-PI's responsibilities, project milestones/deliverables/key performance indicators, reporting (research performance and financial) requirements and amount of funding awarded. PIs must understand and accept the terms and conditions specified in the Award Letter/Funding Agreement as they are responsible for the overall project and management of the grant.

ODPRT will guide the PI on how to go about accepting the grant. Some programmes may require the PI to scrub the approved budget before the grantor releases the formal Letter of Award.

For help, please contact the officer in charge of the programme
""",
    """Multiple WBS accounts for a single grant are exceptions rather than the norm. The identification of co-PI(s) in a grant proposal does not immediately justify the creation of multiple WBS accounts. The Lead PI (as named in the official Letter of Award or Funding Agreement) who wishes to request for multiple WBS accounts for better management of the grant, or to sub-award part of the main grant to co-PI(s) overseeing specific work packages must submit a formal request to Director, Research Administration, ODPRT, through the Department and VDR/Director. The request must discuss the following in detail:
1.	What is the impact in terms of administrative ease for both the PI and administrators?
2.	What is the feasible arrangement proposed by the PI to ensure a real reduction in administrative effort for both PIs and administrators?
3.	What is the PI's proposed workflow and formalised procedure to mitigate risk and ensure proper monitoring of funds to guard against unauthorised use?
4.	How will PI maintain overall control over fund utilisation for all WBS accounts to ensure expenses adhere to the T&Cs of the grantor and Agreement?
Only requests that are strongly supported by the Faculty/RIC/RCE and have addressed all relevant areas will be assessed. Note that if the grantor declines to reimburse NUS for expenses incurred due to violation of the grant’s terms and conditions, the PI and/or host Department/Faculty/RIC/RCE may be required to bear the cost of the rejected claims.

PIs are reminded that they are fully accountable for the overall project and utilisation of the total grants awarded. This duty does not diminish with the sub-division of the grant and PIs are responsible for the entire grant, including the portions sub-awarded to their co-PI(s). Research grants awarded for a single project administered in multiple WBS accounts are governed by the same terms & conditions and remain the sole responsibility of the PI who accepted the grant.

For help, please contact the officer in charge of the programme.

""",
    """PIs are required to submit annual progress reports to grantors to update them on the progress of their research. PIs should refer to the respective grant programme for the details and form in which these are submitted.

Please contact the officer in charge of the programme. 
""",
    """In consideration of the increased risk of payment defaults, PIs/Faculties/Departments/Research Institutes/Centres are required to seek advance payment from the non-government organisation either in full or in progressive stages ahead of milestone deliverables.

The requirement for advance payment must be incorporated into the agreements with non-government organisations. PIs must ensure that work related to a particular milestone does not commence until NUS has received the advance payment for that milestone in full.

To mitigate the risk of payment defaults, the budget reflected in project accounts created to manage grants from non-government organisations and industry funders will be based on the actual cash received from the external party.

Waiver of advance payment requires the prior approval of the Deputy President (Research & Technology). Requests for such waivers must be accompanied by justifications from the PI, HOD and VDR/Centre Director. In the event of a payment default, the PI, Department and Faculty/Centre will be required to bear the costs incurred.

Advance payment is not required for grants received directly (not through subawards) from the following agencies/organisations:
•	Singapore governmental organisations (e.g. PUB, NParks, EDB, MINDEF, etc.)
•	Singapore public sector organisations (e.g. various entities under National Health Group, SingHealth and National University Health Systems, Research Institutes under A*STAR, etc.)
•	Charities and non-profit organisations

For help, please contact the officer in charge of the programme.
""",
]

AGREEMENT_TYPE_QUERIES = [
    """I will be working with an external company on a project. Who can I contact to get more information on the type of agreement required?""",
    """I wish to extend an existing research agreement or my research project, who should I contact? What should I do?""",
    """When is a Research Collaboration Agreement (RCA) required?""",
    """When do I need a Contract Research Agreement (CRA)?""",
    """What is the difference between Research Collaboration Agreement (RCA) and Contract Research Agreement (CRA)? """

]

AGREEMENT_TYPE_GROUND_TRUTH = [
    """Is your agreement research related? If yes, please refer to ODPRT - Research Agreements for more information on types of agreement.  

If your agreement is not research related, please contact the relevant offices below: 
(a) Intellectual Property (IP) matters, IP agreement, Materials Transfer, outgoing Data transfer, NUS IP licences; contact Technology Transfer and Innovation office (TTI) - Contract-Admin@nus.edu.sg 

(b) General legal advice, non-research /academic/student related agreements, incoming data transfer (for research or otherwise), in-licensing of data/software/IP, provision of services (non-research), employment agreements; contact Office of Legal Affairs (OLA) – olasec@nus.edu.sg

(c) procurement (for research or non-research services/goods): contact central Procurement Office (CPO) – askcpo@nus.edu.sg.

Please contact IEP-Admin if you have further queries.""",
    """Please submit your request to IEP Contracting Hub and a IEP case officer will be assigned to assist you. If you do not have access to IEP Contracting Hub, please contact IEP-Admin for a user account to be created.

If in doubt, you may contact IEP-Admin before submitting your request to IEP Contracting Hub.""",
    """Research Collaboration Agreement (RCA) is typically needed in the following scenarios:
(a)	Joint research projects: where NUS and your collaborator(s) are working together on a research project. The RCA will outline the terms of the collaboration, including roles, responsibilities, and contributions NUS and your collaborator(s).   
(b)	Grant support research projects: the joint research project is supported by an external research grant and your collaborator(s) is/are identified in the research grant proposal. 
(c)	Sharing of resources: IP, confidential information or data, materials equipment, facilities etc. that may be shared by NUS and your collaborator(s) for the joint research project.
(d)	Funding and financial support: If there is financial support or funding involved, the agreement should specify how funds will be allocated, managed, and reported. 
A research collaboration agreement helps prevent misunderstandings and provides a clear framework for how the research will be conducted and managed. 
""",
"""Contract Research Agreement (CRA) is typically needed if your collaborator is providing funding to NUS for a research project and expects to own all intellectual property rights that may arise from the research project. 

Under a CRA arrangement, NUS is providing a contracted research services – it is no longer a “collaboration”, and NUS’ costs (except for PI’s salary if already funded by core funding) must be fully borne by your collaborator.  In addition, 60% indirect research costs (IRC) are applicable.

CRAs are NOT encouraged if the research project to be conducted requires NUS to put in significant intellectual / inventive inputs and/or has the potential to create novel IP and know-how which NUS should retain rights to advance its own research capabilities. Typically, CRA are meant for research projects which require only incremental or minor intellectual inputs / expertise from NUS.
""",
"""Research Collaboration Agreement (RCA) is to govern the collaborative research project and which include terms relating to confidentiality, IP rights, publication, liabilities etc.

Research Collaboration Agreement (RCA) is typically needed in the following scenarios:
(a)	Joint research projects: where NUS and your collaborator(s) are working together on a research project. The RCA will outline the terms of the collaboration, including roles, responsibilities, and contributions NUS and your collaborator(s).   
(b)	Grant support research projects: the joint research project is supported by an external research grant and your collaborator(s) is/are identified in the research grant proposal. 
(c)	Sharing of resources: IP, confidential information or data, materials equipment, facilities etc. that may be shared by NUS and your collaborator(s) for the joint research project.
(d)	Funding and financial support: If there is financial support or funding involved, the agreement should specify how funds will be allocated, managed, and reported. 
A research collaboration agreement helps prevent misunderstandings and provides a clear framework for how the research will be conducted and managed.

Contract Research Agreement (CRA) is to govern contracted research project. It is typically needed if your collaborator is providing funding to NUS for a research project and expects to own all intellectual property rights that may arise from the research project. 

Under a CRA arrangement, NUS is providing a contracted research services – it is no longer a “collaboration”, and NUS’ costs (except for PI’s salary if already funded by core funding) must be fully borne by your collaborator.  In addition, 60% indirect research costs (IRC) are applicable.

CRAs are NOT encouraged if the research project to be conducted requires NUS to put in significant intellectual / inventive inputs and/or has the potential to create novel IP and know-how which NUS should retain rights to advance its own research capabilities. Typically, CRA are meant for research projects which require only incremental or minor intellectual inputs / expertise from NUS.
"""
]

GENERAL_QUERIES = [
    """My collaborator is asking for NUS (NDA/RCA/CRA/MOU) template. Where can I find them?""",
    """My faculty/unit is collaborating with another faculty/unit in NUS for a project. Do we need a contract or an agreement for this collaboration?""",
    """Can there be more than one NUS Investigator for a project?""",
    """Can we get the research collaboration agreement (RCA) process started before ethics or IRB approval?""",
    """My industry collaborator would like to have a research agreement where a fee-for- service arrangement would be made, would such engagement fall under Consultation Work, or a Contract Research Agreement?"""

]

GENERAL_GROUND_TRUTH = [
    """Is the template that you are requesting related to research? If yes, you may submit your request to IEP Contracting Hub  If you do not have access to IEP Contracting Hub, please contact IEP-Admin for a user account to be created.

If the template that you are requested is not research related, please contact the relevant offices below: 

(a) Intellectual Property (IP) matters, IP agreement, Materials Transfer, outgoing Data transfer, NUS IP licences; contact Technology Transfer and Innovation office (TTI) - Contract-Admin@nus.edu.sg

(b) General legal advice, non-research /academic/student related agreements, incoming data transfer (for research or otherwise), in-licensing of data/software/IP, provision of services (non-research), employment agreements; contact Office of Legal Affairs (OLA) – olasec@nus.edu.sg 

(c) procurement (for research or non-research services/goods): contact central Procurement Office (CPO) – askcpo@nus.edu.sg 

Please contact IEP-Admin if you have further queries. 
""",
"""No. Formal legal agreement is not required for department/school/ unit/ faculty within NUS as they are part of NUS, provided that it does not involve any external party (outside of NUS).  

If there are any matters that the 2 NUS department/school/ unit/ faculty wish to agree amongst themselves, then the respective Directors or Head of Department or Dean can set out the understanding in writing via an email or letter and do not require IEP review. 
""",
"""Yes, however for most projects, a lead investigator is to be identified as the Principal Investigator and the other investigators can be the Co-Principal Investigators.""",
"""Yes, IEP can start to draft or review the research collaboration agreement before ethics or IRB is approved. Please submit your request to IEP Contracting Hub. If you do not have access to IEP Contracting Hub, please contact IEP-Admin for a user account to be created.
However, it would be preferred if IRB is approved prior to signing the agreement.
""",
"""If the work is intended to be undertaken by you in your personal capacity as a consultant, please refer to the Consultation Work Scheme policy. NUS will not review or advise on any private consultancy agreements.
 
Fee-for-service projects with research components to be undertaken by NUS (and not you as a private consultant) fall under Contract Research are unlikely to require significant intellectual inputs from NUS. Such projects require a minimum Indirect Research Costs (IRC) of 60%.
"""
]

IEP_CONRACTING_HUB_QUERIES = [
    """What is IEP Contracting Hub?""",
    """How do I create an account in IEP Contracting Hub?""",
    """Can IEP Contracting Hub be used by anyone in NUS? """
]

IEP_CONTRACTING_HUB_GROUND_TRUTH = [
    """The Contracting Hub (by Pactly) is hosted in ODPRT where PIs/researchers/faculty-admin (“Requesters”) can submit agreement requests online and provide necessary information and/or upload draft agreements received from external collaborators through Contracting Hub. 
 
In addition to submission of agreement requests, the Contracting Hub is a one-stop web portal where Requesters can:
1.	request/download for NUS standard template agreements for research; 
2.	track status of all their requests for research agreements (from first request to negotiation to execution); 
3.	view/download executed agreements; and
4.	get in touch with IEP directly via the Contracting Hub.""",
"""Please contact IEP-Admin for a user account to be created.""",
"""The IEP Contracting Hub can be used by any personnel of NUS (e.g. Principal Investigator, administrators, students) except for Yong Loo Lin School of Medicine.  
If your representing faculty/unit/department is within Yong Loo Lin School of Medicine, please contact IEP-Admin for further advice.
"""
]

REDIRECT_TTI_QUERIES = [
    """What is NUS’s policy on intellectual property (IP)?""",
    """Who do I contact if I have an invention to disclose?""",
    """Who do I contact for materials transfer from or to another party for research purposes?""",
    """I have a data transfer agreement. who should I send for review?"""
]

REDIRECT_TTI_GROUND_TRUTH = [
    """Please find more details related to Intellectual Property (IP) matters @
FAQs & Policies and Guidelines (nus.edu.sg)
""", 
"""Please contact NUS Enterprise – Technology Transfer and Innovation at Contract-Admin@nus.edu.sg if you have further queries.

You may find more details @ https://nus.edu.sg/tti/for-researchers/disclosing-an-invention
""",
"""Please contact NUS Enterprise – Technology Transfer and Innovation at Contract-Admin@nus.edu.sg 

You may find more details @ Agreement for Researchers (nus.edu.sg)
""",
"""For incoming data transfer (e.g. NUS is receiving data from collaborator), please contact Office of Legal Affairs (OLA) at olasec@nus.edu.sg 

For outgoing data transfer (e.g. NUS is providing data to collaborator), please contact NUS Enterprise – Technology Transfer and Innovation at Contract-Admin@nus.edu.sg 
"""
]

REDIRECT_OLA_QUERIES = [
    """Who do I contact for student related matters?""",
    """Who do I contact if my collaborator is providing services for my project?""",
    """My collaborator is transferring data to me, what agreement do I need?""",
    """Are there any procedures involving Tenders for my project?""",
    """Who do I contact for advice regarding purchase or procurement services (research or otherwise) / goods / equipment or leasing for equipment for research?"""
]

REDIRECT_OLA_GROUND_TRUTH = [
    """Please contact Office of Legal Affairs (OLA) at olasec@nus.edu.sg""",
    """Please contact Office of Legal Affairs (OLA) at olasec@nus.edu.sg""",
    """For incoming data transfer (e.g. NUS is receiving data from collaborator), please contact Office of Legal Affairs (OLA) at olasec@nus.edu.sg 

For outgoing data transfer (e.g. NUS is providing data to collaborator), please contact NUS Enterprise – Technology Transfer and Innovation at Contract-Admin@nus.edu.sg
""",
"""Please find more details related to tender @
NUS Office of Legal Affairs Homepage 
""",
"""Please contact Central Procurement Office (CPO) at askcpo@nus.edu.sg 

You may find more details @https://proctor.nus.edu.sg/policy/
"""
]

REDIRECT_IRB_QUERIES = [
    """Who can I contact for ethics approval or ethics exemption or Institutional Review Board (IRB) matters?""",
    """Do I need to apply for IRB or ethics approval?"""
]

REDIRECT_IRB_GROUND_TRUTH = [
    """Please contact IRB at  irb@nus.edu.sg 
You may find more details @ Home (nus.edu.sg)
""",
"""You will need ethics approval if your research project involves human subject participation and/or human tissues / cells/ use of data / health information or biological materials obtained from or pertaining to any human subject.

For more information, you may refer to IRB Homepage or write to irb@nus.edu.sg.
"""
]

PRE_AWARD_QUERIES = [
    """Am I eligible to apply for a grant as PI or Co-PI?""",
    """Where can I find grant or funding available in NUS? """,
    """I want to apply for external funding. How do I go about doing it? """
]

PRE_AWARD_GROUND_TRUTH = [
    """A funding agency may impose eligibility criteria that must be met by an applicant who wishes to act as the PI and/or co-PI of a proposed research project. Details on eligibility criteria are outlined in the grant call guidelines. Typically, the major grant agencies (MOE, NRF, NMRC, A*STAR) require PIs and co-PIs to be “full-time faculty” of NUS. “Full-time faculty” are those who hold appointments and perform duties at NUS for a minimum of 9 months a year.

Additional clearance from the Deputy President (Research & Technology) (DPRT) through the Director, Research Administration (DRA) is required if the applicant for PI or co-PI meets the grantor’s eligibility criteria but:
•	Does not have a NUS* contract covering the full proposed project duration;
•	Is a Research Track or Executive & Administrative staff (e.g. deputy director, research fellow, senior research fellow); and/or,
•	Does not hold a full-time appointment with NUS (e.g. emeritus, adjunct and visiting staff, partial and part-time NUS appointment).

*Research staff who are interested to apply for research grants should note that funding agencies require partial charging of their salaries to account for time not spent performing the research funded by the agency.

For more information, please contact the officer in charge of the programme.
""",
"""The Office of the Deputy President (Research & Technology) issues a monthly newsletter that lists funding opportunities available to NUS researchers.

Researchers may visit NUS’ grant call portal, InfoReady, to view details of open grant calls.

NUS also offers internal programmes such as Humanities and Social Science Fellowships and Start-Up Grants to help new staff kick-off and build their research base at NUS.

Since many grantors strongly discourage researchers from submitting a single proposal to multiple funding agencies for funding consideration, PIs should make a calculated decision before sending in their applications.

For help, please contact the officer in charge of the programme.
""",
"""All applications for external funding must be endorsed by the Department and Faculty and submitted through ODPRT.
Applicants should refer closely to the Grant Call guidelines and application instructions since they may differ with each programme. In general, a complete application package should contain
•	Research Compliances and Resources (RCR) Form
o	Required for single stage grant calls and at the full proposal stage of two-stage grant calls
o	Not required for Whitepaper and Letter of Intent (LOI) stage of two-stage grant calls
o	The RCR form must be endorsed by the VDR/Director RIC/RCE. HOD support is additionally required if the applicant’s contract does not cover the proposed project duration.
•	Research proposal, statement of research intent
•	Other supporting documents as specified in the Grant Call Guidelines, e.g. quotations, curriculum vitae of project members, etc.
All applications for external research funding must provide for IRC.
A minimum rate of 30% is levied on the total direct research cost of sponsored research grants supported by public sector agencies, industry and/or other external parties.
A higher rate of at least 60% of the total direct project cost is applicable to Contract Research (fee-for-service) commissioned by public sector agencies, industry and/or other external parties.
PIs must ensure that the NUS External Grants Indirect Research Cost Recovery (IRC) Policy is communicated to potential external grantors/collaborators from the point of negotiations.
"""
]

POST_AWARD_QUERIES = [
    """How am I notified when I have been awarded the grant?""",
    """Do I need to ask for advance payment for the funding that my collaborator is giving me?""",
    """How do I apply for multiple WBS account?""",
    """Who do I submit my progress report to?""",
    """I am leaving NUS. How do I handover my grant and/or Project?  """
]

POST_AWARD_GROUND_TRUTH = [
    """Research funding awarded to NUS staff and hosted by NUS may be conveyed:
•	Through online portals and grant management systems (e.g. NRF’s IGMS, A*STAR’s iGrants, NIE ROMS, etc.)
•	Via email in softcopy – Letter of Awards, Funding Agreements
The Grant Award Letter or Funding Agreement details the Host Institution and PI/Co-PI’s responsibilities, project milestones/deliverables/key performance indicators, reporting (research performance and financial) requirements and amount of funding awarded. PIs must understand and accept the terms and conditions specified in the Award Letter/Funding Agreement as they are responsible for the overall project and management of the grant.

ODPRT will guide the PI on how to go about accepting the grant. Some programmes may require the PI to scrub the approved budget before the grantor releases the formal Letter of Award.

For help, please contact the officer in charge of the programme
""",
"""In consideration of the increased risk of payment defaults, PIs/Faculties/Departments/Research Institutes/Centres are required to seek advance payment from the non-government organisation either in full or in progressive stages ahead of milestone deliverables.

The requirement for advance payment must be incorporated into the agreements with non-government organisations. PIs must ensure that work related to a particular milestone does not commence until NUS has received the advance payment for that milestone in full.

To mitigate the risk of payment defaults, the budget reflected in project accounts created to manage grants from non-government organisations and industry funders will be based on the actual cash received from the external party.

Waiver of advance payment requires the prior approval of the Deputy President (Research & Technology). Requests for such waivers must be accompanied by justifications from the PI, HOD and VDR/Centre Director. In the event of a payment default, the PI, Department and Faculty/Centre will be required to bear the costs incurred.

Advance payment is not required for grants received directly (not through subawards) from the following agencies/organisations:
•	Singapore governmental organisations (e.g. PUB, NParks, EDB, MINDEF, etc.)
•	Singapore public sector organisations (e.g. various entities under National Health Group, SingHealth and National University Health Systems, Research Institutes under A*STAR, etc.)
•	Charities and non-profit organisations

For help, please contact the officer in charge of the programme.
""",
"""Multiple WBS accounts for a single grant are exceptions rather than the norm. The identification of co-PI(s) in a grant proposal does not immediately justify the creation of multiple WBS accounts. The Lead PI (as named in the official Letter of Award or Funding Agreement) who wishes to request for multiple WBS accounts for better management of the grant, or to sub-award part of the main grant to co-PI(s) overseeing specific work packages must submit a formal request to Director, Research Administration, ODPRT, through the Department and VDR/Director. The request must discuss the following in detail:
1.	What is the impact in terms of administrative ease for both the PI and administrators?
2.	What is the feasible arrangement proposed by the PI to ensure a real reduction in administrative effort for both PIs and administrators?
3.	What is the PI's proposed workflow and formalised procedure to mitigate risk and ensure proper monitoring of funds to guard against unauthorised use?
4.	How will PI maintain overall control over fund utilisation for all WBS accounts to ensure expenses adhere to the T&Cs of the grantor and Agreement?
Only requests that are strongly supported by the Faculty/RIC/RCE and have addressed all relevant areas will be assessed. Note that if the grantor declines to reimburse NUS for expenses incurred due to violation of the grant’s terms and conditions, the PI and/or host Department/Faculty/RIC/RCE may be required to bear the cost of the rejected claims.

PIs are reminded that they are fully accountable for the overall project and utilisation of the total grants awarded. This duty does not diminish with the sub-division of the grant and PIs are responsible for the entire grant, including the portions sub-awarded to their co-PI(s). Research grants awarded for a single project administered in multiple WBS accounts are governed by the same terms & conditions and remain the sole responsibility of the PI who accepted the grant.

For help, please contact the officer in charge of the programme.
""",
"""PIs are required to submit annual progress reports to grantors to update them on the progress of their research. PIs should refer to the respective grant programme for the details and form in which these are submitted.

Please contact the officer in charge of the programme. 
""",
"""Staff who are leaving NUS are required to complete a checklist for all research projects ongoing and completed within the last 6 months. The checklist is to ensure that the staff has taken the necessary actions such as the handover of ongoing projects, transfer of staff/student supervisory obligations, and closure of research protocols prior to their departure from the University.

Outbound staff should notify the relevant research compliance office (IRB, DERC, IACUC, CM) prior to their departure to ensure smooth transition/closure of protocols.

For project transfer cases, the WBSes may be “Locked” to prevent further transactions until formal approval has been obtained from the funding agency for the change in PI or transfer of the project to another institution.

Checklists should be cleared by the HOD (or nominee) prior to submission to the Office of Human Resources, copied to ODPRT, VDR and NUS Enterprise.

The requirement for submission of the Handover Checklist is incorporated into OHR’s Notes for Staff Leaving Service located in the NUS Staff Intranet.

For help, please contact the officer in charge of the programme.
"""
]