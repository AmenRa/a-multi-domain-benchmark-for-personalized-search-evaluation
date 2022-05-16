#!/bin/bash

LIGHT_GREEN='\033[1;32m'
LIGHT_BLUE='\033[1;34m'
NO_COLOR='\033[0m'

THREADS=$(($(nproc) / 2))

# Create temporary folder
mkdir -p tmp
mkdir -p tmp/archives

# Download AMiner v12 dataset
printf "${LIGHT_BLUE}Starting MAG download...\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting Affiliations download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/01.Affiliations.nt.bz2?download=1 -O tmp/archives/01.Affiliations.nt.bz2
printf "${LIGHT_GREEN}Affiliations download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting Authors download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/02.Authors.nt.bz2?download=1 -O tmp/archives/02.Authors.nt.bz2
printf "${LIGHT_GREEN}Authors download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting ConferenceInstances download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/03.ConferenceInstances.nt.bz2?download=1 -O tmp/archives/03.ConferenceInstances.nt.bz2
printf "${LIGHT_GREEN}ConferenceInstances download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting ConferenceSeries download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/04.ConferenceSeries.nt.bz2?download=1 -O tmp/archives/04.ConferenceSeries.nt.bz2
printf "${LIGHT_GREEN}ConferenceSeries download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting Journals download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/05.Journals.nt.bz2?download=1 -O tmp/archives/05.Journals.nt.bz2
printf "${LIGHT_GREEN}Journals download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperAuthorAffiliations download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/06.PaperAuthorAffiliations.nt.bz2?download=1 -O tmp/archives/06.PaperAuthorAffiliations.nt.bz2
printf "${LIGHT_GREEN}PaperAuthorAffiliations download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperExtendedAttributes download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/07.PaperExtendedAttributes.nt.bz2?download=1 -O tmp/archives/07.PaperExtendedAttributes.nt.bz2
printf "${LIGHT_GREEN}PaperExtendedAttributes download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperReferences download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/08.PaperReferences.nt.bz2?download=1 -O tmp/archives/08.PaperReferences.nt.bz2
printf "${LIGHT_GREEN}PaperReferences download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperResources download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/09.PaperResources.nt.bz2?download=1 -O tmp/archives/09.PaperResources.nt.bz2
printf "${LIGHT_GREEN}PaperResources download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting Papers download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/10.Papers.nt.bz2?download=1 -O tmp/archives/10.Papers.nt.bz2
printf "${LIGHT_GREEN}Papers download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperUrls download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/11.PaperUrls.nt.bz2?download=1 -O tmp/archives/11.PaperUrls.nt.bz2
printf "${LIGHT_GREEN}PaperUrls download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting EntityRelatedEntities download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/12.EntityRelatedEntities.nt.bz2?download=1 -O tmp/archives/12.EntityRelatedEntities.nt.bz2
printf "${LIGHT_GREEN}EntityRelatedEntities download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting FieldOfStudyChildren download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/13.FieldOfStudyChildren.nt.bz2?download=1 -O tmp/archives/13.FieldOfStudyChildren.nt.bz2
printf "${LIGHT_GREEN}FieldOfStudyChildren download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting FieldOfStudyExtendedAttributes download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/14.FieldOfStudyExtendedAttributes.nt.bz2?download=1 -O tmp/archives/14.FieldOfStudyExtendedAttributes.nt.bz2
printf "${LIGHT_GREEN}FieldOfStudyExtendedAttributes download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting FieldsOfStudy download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/15.FieldsOfStudy.nt.bz2?download=1 -O tmp/archives/15.FieldsOfStudy.nt.bz2
printf "${LIGHT_GREEN}FieldsOfStudy download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperFieldsOfStudy download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/16.PaperFieldsOfStudy.nt.bz2?download=1 -O tmp/archives/16.PaperFieldsOfStudy.nt.bz2
printf "${LIGHT_GREEN}PaperFieldsOfStudy download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperRecommendations download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/17.PaperRecommendations.nt.bz2?download=1 -O tmp/archives/17.PaperRecommendations.nt.bz2
printf "${LIGHT_GREEN}PaperRecommendations download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting RelatedFieldOfStudy download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/18.RelatedFieldOfStudy.nt.bz2?download=1 -O tmp/archives/18.RelatedFieldOfStudy.nt.bz2
printf "${LIGHT_GREEN}RelatedFieldOfStudy download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperCitationContexts download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/19.PaperCitationContexts.nt.bz2?download=1 -O tmp/archives/19.PaperCitationContexts.nt.bz2
printf "${LIGHT_GREEN}PaperCitationContexts download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperTags download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/21.PaperTags.nt.bz2?download=1 -O tmp/archives/21.PaperTags.nt.bz2
printf "${LIGHT_GREEN}PaperTags download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperFieldsOfStudyNew download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/22.PaperFieldsOfStudyNew.nt.bz2?download=1 -O tmp/archives/22.PaperFieldsOfStudyNew.nt.bz2
printf "${LIGHT_GREEN}PaperFieldsOfStudyNew download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting Authors_disambiguated download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/23.Authors_disambiguated.nt.bz2?download=1 -O tmp/archives/23.Authors_disambiguated.nt.bz2
printf "${LIGHT_GREEN}Authors_disambiguated download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting PaperAuthorAffiliations_disambiguated download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/24.PaperAuthorAffiliations_disambiguated.nt.bz2?download=1 -O tmp/archives/24.PaperAuthorAffiliations_disambiguated.nt.bz2
printf "${LIGHT_GREEN}PaperAuthorAffiliations_disambiguated download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting AuthorORCID download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/4617285/files/25.AuthorORCID.nt.bz2?download=1 -O tmp/archives/25.AuthorORCID.nt.bz2
printf "${LIGHT_GREEN}AuthorORCID download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting abstracts download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/3936556/files/PaperAbstracts.nt.bz2?download=1 -O tmp/archives/PaperAbstracts.nt.bz2
printf "${LIGHT_GREEN}Abstracts download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_BLUE}Starting papers' lang download...\n${NO_COLOR}"
wget -c https://zenodo.org/record/3936556/files/PaperLanguages.nt.bz2?download=1 -O tmp/archives/PaperLanguages.nt.bz2
printf "${LIGHT_GREEN}Papers' lang download: DONE\n\n${NO_COLOR}"

printf "${LIGHT_GREEN}MAG download: DONE\n\n${NO_COLOR}"