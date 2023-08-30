# Define a function to extract the value between two "|" symbols in the ANN field
def extract_ann_value(ann):
    parts = ann.split("|")
    if len(parts) >= 2:
        return parts[1]
    else:
        return ""

# Define a function to determine the REGION based on ANN
def determine_region(ann):
    if "intergenic_region" in ann:
        return "intergenic_region"
    else:
        return "genic_region"

# Get input and output filenames from user
input_filename = input("Enter the input VCF filename: ")
output_filename = input("Enter the output filename for results: ")

# Open and read the input VCF file
with open(input_filename, "r") as vcf_file, open(output_filename, "w") as output_file:
    output_file.write("{:<10} {:<10} {:<5} {:<5} {:<10} {:<5} {:<5} {:<10} {:<20} {:<15}\n".format("CHROM", "POS", "REF", "ALT", "QUAL", "DP", "AF", "TYPE", "ANN", "REGION"))
    output_file.write("="*90 + "\n")
    
    for line in vcf_file:
        if line.startswith("#CHROM"):
            continue
        if not line.startswith("#"):
            parts = line.strip().split("\t")
            chrom = parts[0]
            pos = parts[1]
            ref = parts[3]
            alt = parts[4]
            qual = parts[5]
            info = parts[7]

            # Split INFO field into key-value pairs
            info_dict = {}
            for item in info.split(";"):
                key, value = item.split("=")
                info_dict[key] = value

            # Extract required values from INFO
            dp = info_dict.get("DP", "")
            af = info_dict.get("AF", "")
            variant_type = info_dict.get("TYPE", "")
            ann = info_dict.get("ANN", "")
            ann_value = extract_ann_value(ann)
            region = determine_region(ann_value)

            output_file.write("{:<10} {:<10} {:<5} {:<5} {:<10} {:<5} {:<5} {:<10} {:<20} {:<15}\n".format(chrom, pos, ref, alt, qual, dp, af, variant_type, ann_value, region))

print("Results have been written to", output_filename)
