#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <regex.h>        
#include <string.h>

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
        //printf("range %zd - %zd matches\n",
        //       offset + whole_match.rm_so,
        //       offset + whole_match.rm_eo);
        offset += whole_match.rm_eo;
        if (whole_match.rm_so == whole_match.rm_eo) {
            offset += 1;
        }
        if (offset > length) {
            break;
        }
    }
    if (! match) {
        printf("\"%s\" does not contain a match\n", sz);
    }
    return ctr; 
}

int main(int argc, char *argv[])
{
    if(argc < 2) 
        return 1;
    
    FILE * fp;
    FILE * fw;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    
    regex_t gene_regex;
    regex_t protein_regex;
    regex_t chemical_regex;
    regex_t disease_regex;
    regex_t statement_regex;
    regex_t human_gene_regex;
    regex_t acid_regex;
    int reti;
    int gene_match = 0;
    int protein_match = 0;
    int chemical_match = 0;
    int disease_match = 0;
    int human_gene_match = 0;
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
    reti = regcomp(&human_gene_regex, "\"property\":\"P31\".*\"entity-type\":\"item\",\"numeric-id\":106291923", 0);
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
    fw = fopen("list_instances_of_genes.csv", "w");
    if (fp == NULL)
        exit(EXIT_FAILURE);
    int item_statements = 0;
    while ((read = getline(&line, &len, fp)) != -1) {
        item_statements = num_of_match(&statement_regex, line);
        reti = regexec(&gene_regex, line, 0, NULL, 0);
        if (!reti) {
            gene_match++;
            gene_statements += item_statements;
            fprintf(fw, "%.*s\n",40,line);
        }
        reti = regexec(&protein_regex, line, 0, NULL, 0);
        if (!reti) {
            protein_match++;
            protein_statements += item_statements;
        }
        reti = regexec(&chemical_regex, line, 0, NULL, 0);
        if (!reti) {
            chemical_match++;
            chemical_statements += item_statements;
        }
        reti = regexec(&disease_regex, line, 0, NULL, 0);
        if (!reti) {
            disease_match++;
            disease_statements += item_statements;
        }
        reti = regexec(&human_gene_regex, line, 0, NULL, 0);
        if (!reti) {
            human_gene_match++;
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
    fprintf(stderr, "Human Genes: %d\n",human_gene_match);
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
    regfree(&human_gene_regex);
    regfree(&acid_regex);
    fclose(fp);
    if (line)
        free(line);
    exit(EXIT_SUCCESS);
}
