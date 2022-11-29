#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <regex.h>        
#include <string.h>

// counts the number of occurrences of a regex in a line
// thanks to https://stackoverflow.com/questions/36975020/count-number-of-matches-using-regex-h-in-c
int num_of_match(regex_t *pexp, char *sz) {
    regmatch_t whole_match;
    int eflags = 0;
    int match = 0;
    int ctr = 0;
    size_t offset = 0;
    size_t length = strlen(sz);
    while (regexec(pexp, sz + offset, 1, &whole_match, eflags) == 0) {
        eflags = REG_NOTBOL;
        match = 1;
        ctr += 1;
        offset += whole_match.rm_eo;
        if (whole_match.rm_so == whole_match.rm_eo) {
            offset += 1;
        }
        if (offset > length) {
            break;
        }
    }
    return ctr; 
}

int main(int argc, char *argv[])
{
    if(argc < 2) 
        return 1;
    
    FILE *fp, *fw_genes, *fw_proteins, *fw_chemicals, *fw_diseases;
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    
    regex_t gene_regex;
    regex_t protein_regex;
    regex_t chemical_regex;
    regex_t disease_regex;
    regex_t statement_regex;
    regex_t operon_regex;
    regex_t acid_regex;
    int reti;
    int gene_match = 0;
    int protein_match = 0;
    int chemical_match = 0;
    int disease_match = 0;
    int operon_match = 0;
    int acid_match = 0;
    int gene_statements = 0;
    int protein_statements = 0;
    int chemical_statements = 0;
    int disease_statements = 0;
    int all_statements = 0;
    char msgbuf[100];
    
    reti = regcomp(&gene_regex, "\"property\":\"P31\".*\"entity-type\":\"item\",\"numeric-id\":7187", 0);
    if (reti) {
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }
    reti = regcomp(&protein_regex, "\"property\":\"P31\".*\"entity-type\":\"item\",\"numeric-id\":8054", 0);
    if (reti) {
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }
    reti = regcomp(&chemical_regex, "\"property\":\"P31\".*\"entity-type\":\"item\",\"numeric-id\":11173", 0);
    if (reti) {
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }
    reti = regcomp(&disease_regex, "\"property\":\"P31\".*\"entity-type\":\"item\",\"numeric-id\":12136", 0);
    if (reti) {
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }
    reti = regcomp(&operon_regex, "\"property\":\"P31\".*\"entity-type\":\"item\",\"numeric-id\":139677", 0);
    if (reti) {
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }
    reti = regcomp(&acid_regex, "\"property\":\"P31\".*\"entity-type\":\"item\",\"numeric-id\":11158", 0);
    if (reti) {
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }
    reti = regcomp(&statement_regex, "\"type\":\"statement\"", 0);//.*\",\"rank\":", 0);
    if (reti){
        fprintf(stderr, "Could not compile regex\n");
        exit(1);
    }

    
    fp = fopen(argv[1], "r");
    fw_genes = fopen("list_instances_of_genes.csv", "w");
    fw_proteins = fopen("list_instances_of_proteins.csv", "w");
    fw_chemicals = fopen("list_instances_of_chemical_compounds.csv", "w");
    fw_diseases = fopen("list_instances_of_diseases.csv", "w");
    if (fp == NULL)
        exit(EXIT_FAILURE);
    int item_statements = 0;
    while ((read = getline(&line, &len, fp)) != -1) {
        item_statements = num_of_match(&statement_regex, line);
        reti = regexec(&gene_regex, line, 0, NULL, 0);
        if (!reti) {
            gene_match++;
            gene_statements += item_statements;
            fprintf(fw_genes, "%.*s\n",40,line);
        }
        reti = regexec(&protein_regex, line, 0, NULL, 0);
        if (!reti) {
            protein_match++;
            protein_statements += item_statements;
            fprintf(fw_proteins, "%.*s\n",40,line);
        }
        reti = regexec(&chemical_regex, line, 0, NULL, 0);
        if (!reti) {
            chemical_match++;
            chemical_statements += item_statements;
            fprintf(fw_chemicals, "%.*s\n",40,line);
        }
        reti = regexec(&disease_regex, line, 0, NULL, 0);
        if (!reti) {
            disease_match++;
            disease_statements += item_statements;
            fprintf(fw_diseases, "%.*s\n",40,line);
        }
        reti = regexec(&operon_regex, line, 0, NULL, 0);
        if (!reti) {
            operon_match++;
        }
        reti = regexec(&acid_regex, line, 0, NULL, 0);
        if (!reti) {
            acid_match++;
        }
        all_statements += item_statements;
    }
    fprintf(stderr, "Genes: %d\n",gene_match);
    fprintf(stderr, "Proteins: %d\n",protein_match);
    fprintf(stderr, "Chemical Compounds: %d\n",chemical_match);
    fprintf(stderr, "Diseases: %d\n",disease_match);
    fprintf(stderr, "Operons: %d\n",operon_match);
    fprintf(stderr, "Acids: %d\n",acid_match);
    fprintf(stderr, "\n");
    fprintf(stderr, "Gene Statements: %d\n", gene_statements);
    fprintf(stderr, "Protein Statements: %d\n", protein_statements);
    fprintf(stderr, "Chemical Compound Statements: %d\n", chemical_statements);
    fprintf(stderr, "Disease Statements: %d\n", disease_statements);
    fprintf(stderr, "\n");
    fprintf(stderr, "All Statements: %d\n", all_statements);
    
    regfree(&gene_regex);
    regfree(&protein_regex);
    regfree(&chemical_regex);
    regfree(&disease_regex);
    regfree(&statement_regex);
    regfree(&operon_regex);
    regfree(&acid_regex);
    fclose(fp);
    fclose(fw_genes);
    fclose(fw_proteins);
    fclose(fw_chemicals);
    fclose(fw_diseases);
    if (line)
        free(line);
    exit(EXIT_SUCCESS);
}
